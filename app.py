from flask import Flask, render_template, request, flash,url_for, redirect
from flask_login import login_required, logout_user, login_user, LoginManager
from database.conexao import Session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.horario import Horario


app = Flask(__name__)

login_manager = LoginManager(app)

app.secret_key = 'SAUANOFODÃO'

@login_manager.user_loader
def load_user(user_id):
    db = Session()
    user = db.get(User, int(user_id))
    db.close()
    return user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        db = Session()
        if db.query(User).filter_by(email=email).first():
            flash('E-mail já cadastrado!')
            db.close()
            return redirect(url_for('cadastro'))

        hashed = generate_password_hash(senha)
        novo_user = User(nome=nome, email=email, senha_hash=hashed)
        db.add(novo_user)
        db.commit()
        db.close()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('login'))

    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        db = Session()
        user = db.query(User).filter_by(email=email).first()

        if not user or not check_password_hash(user.senha_hash, senha):
            flash('E-mail ou senha inválidos.')
            db.close()
            return redirect(url_for('login'))

        login_user(user)
        db.close()
        return redirect(url_for('dashboard'))

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


