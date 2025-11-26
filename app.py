from flask import Flask, render_template, request, flash,url_for, redirect
from flask_login import login_required, logout_user

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')
    return render_template('dashboard.html')


@app.route('/logout')   
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!')
    return redirect(url_for('index'))
