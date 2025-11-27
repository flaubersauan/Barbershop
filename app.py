from flask import Flask, render_template, request, flash,url_for, redirect
from flask_login import login_required, logout_user, login_user, LoginManager
from database.conexao import Session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.horario import Horario
from models.agendamento import Agendamento
from datetime import date, time
from flask_login import current_user
from sqlalchemy.orm import joinedload

app = Flask(__name__)

login_manager = LoginManager(app)

app.secret_key = 'SAUANOFODÃO'

session = Session()

# Horários fixos
horas = [
    time(8, 0),
    time(9, 0),
    time(10, 0),
    time(11, 0),
    time(13, 0),
    time(14, 0),
    time(15, 0),
    time(16, 0),
    time(17, 0),
]

hoje = date.today()

for h in horas:
    existe = session.query(Horario).filter_by(data=hoje, hora=h).first()
    if not existe:
        session.add(Horario(data=hoje, hora=h))

session.commit()
session.close()


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



@app.route('/dashboard')
@login_required
def dashboard():
    db = Session()

    # Carrega todos os horários e também o agendamento
    horarios = (
        db.query(Horario).options(joinedload(Horario.agendamento)).order_by(Horario.hora.asc()).all())
    db.close()

    return render_template("dashboard.html",usuario=current_user.nome,horarios=horarios)


@app.route("/agendar/<int:horario_id>")
@login_required
def agendar(horario_id):
    db = Session()

    horario = db.get(Horario, horario_id)
    if not horario or not horario.disponivel:
        flash("Horário indisponível!")
        db.close()
        return redirect(url_for("dashboard"))

    # Verifica se o usuário já tem agendamento
    if current_user.agendamento:
        flash("Você já possui um horário agendado!")
        db.close()
        return redirect(url_for("dashboard"))

    # Verifica se o horário já está agendado
    if horario.agendamento:
        flash("Este horário já foi reservado!")
        db.close()
        return redirect(url_for("dashboard"))

    # Cria o agendamento
    novo = Agendamento(
        user_id=current_user.id,horario_id=horario.id)

    horario.disponivel = False

    db.add(novo)
    db.commit()
    db.close()

    flash("Agendamento realizado com sucesso!")
    return redirect(url_for("dashboard"))

@app.route('/logout')   
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!')
    return redirect(url_for('index'))


