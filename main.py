from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# URL base da API FastAPI
API_URL = "https://p1-30lp.onrender.com/goals/"
TOTALS_URL = "https://p1-30lp.onrender.com/total/"

@app.route('/')
def index():
    try:
        # Obter todas as metas da API
        response = requests.get(API_URL)
        response.raise_for_status()
        goals = response.json()
        # Obter totais 
        totals_response = requests.get(TOTALS_URL)
        totals_response.raise_for_status()
        totals = totals_response.json()
        return render_template('index.html', goals=goals, totals=totals)
    except Exception as e:
        flash(f"Erro ao carregar metas: {str(e)}", "danger")
        return render_template('index.html', goals=[])

@app.route('/create', methods=['POST'])
def create():
    try:
        # Dados do formulário
        name = request.form['name']
        target_amount = request.form['target_amount']
        current_amount = request.form['current_amount']

        # Enviar requisição para criar nova meta
        payload = {
            "name": name,
            "target_amount": float(target_amount),
            "current_amount": float(current_amount)
        }
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        flash("Meta criada com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao criar meta: {str(e)}", "danger")
    return redirect(url_for('index'))

@app.route('/update/<goal_id>', methods=['POST'])
def update(goal_id):
    try:
        # Dados do formulário
        name = request.form['name']
        target_amount = request.form['target_amount']
        current_amount = request.form['current_amount']

        # Enviar requisição para atualizar meta
        payload = {
            "name": name,
            "target_amount": float(target_amount),
            "current_amount": float(current_amount)
        }
        response = requests.put(f"{API_URL}{goal_id}", json=payload)
        response.raise_for_status()
        flash("Meta atualizada com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao atualizar meta: {str(e)}", "danger")
    return redirect(url_for('index'))

@app.route('/delete/<goal_id>', methods=['POST'])
def delete(goal_id):
    try:
        # Enviar requisição para deletar meta
        response = requests.delete(f"{API_URL}{goal_id}")
        response.raise_for_status()
        flash("Meta deletada com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao deletar meta: {str(e)}", "danger")
    return redirect(url_for('index'))
@app.route('/geral')
def view_totals():
    try:
        totals_response = requests.get(TOTALS_URL)
        totals_response.raise_for_status()
        totals = totals_response.json()
        print(totals)
        return render_template('total.html', totals=totals)
    except Exception as e:
        flash(f"Erro ao carregar totais: {str(e)}", "danger")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
