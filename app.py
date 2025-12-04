from flask import Flask, render_template
from flask_login import login_required,LoginManager
from database.conexao import Session
from models import User, Horario        
from datetime import date, time
from flask_login import current_user
from sqlalchemy.orm import joinedload
from blueprints.auth.routes import auth_bp
from blueprints.agendamentos.routes import agendamento_bp
from blueprints.horarios.routes import horario_bp

app = Flask(__name__)

login_manager = LoginManager(app)

app.secret_key = 'SAUANOFODÃO'

app.register_blueprint(auth_bp)
app.register_blueprint(agendamento_bp)
app.register_blueprint(horario_bp)

session = Session()

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



@app.route('/dashboard')
@login_required
def dashboard():
    db = Session()

    # carrega todos os horários + todos os agendamentos vinculados
    horarios = (
        db.query(Horario)
        .options(joinedload(Horario.agendamento))
        .order_by(Horario.hora.asc())
        .all()
    )

    # agora escolher apenas o agendamento ATIVO
    for h in horarios:
        ativo = None
        for ag in h.agendamento:
            if ag.status == "ativo":
                ativo = ag
                break
        h.agendamento_ativo = ativo   # campo virtual para o template usar

    db.close()

    return render_template("dashboard.html", usuario=current_user.nome, horarios=horarios)

if __name__ == '__main__':
    app.run(debug=True)