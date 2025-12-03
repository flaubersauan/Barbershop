from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.conexao import Session
from models import User
from . import auth_bp

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        db = Session()
        if db.query(User).filter_by(email=email).first():
            flash('E-mail já cadastrado!')
            db.close()
            return redirect(url_for('auth.cadastro'))

        hashed = generate_password_hash(senha)
        novo_user = User(nome=nome, email=email, senha_hash=hashed)
        db.add(novo_user)
        db.commit()
        db.close()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        db = Session()
        user = db.query(User).filter_by(email=email).first()

        if not user or not check_password_hash(user.senha_hash, senha):
            flash('E-mail ou senha inválidos.')
            db.close()
            return redirect(url_for('auth.login'))

        login_user(user)
        db.close()
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@auth_bp.route('/logout')   
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!')
    return redirect(url_for('index'))