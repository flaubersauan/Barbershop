from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from database.conexao import Session
from models import Agendamento
from sqlalchemy.orm import joinedload

from . import agendamento_bp
@agendamento_bp.route("/perfil")
@login_required
def perfil():
    db = Session()

    agendamento = (db.query(Agendamento).options(joinedload(Agendamento.horario))  .filter_by(user_id=current_user.id, status="ativo").first())

    db.close()

    return render_template("perfil.html",usuario=current_user,agendamento=agendamento)


@agendamento_bp.route("/cancelar_agendamento")
@login_required
def cancelar_agendamento():
    db = Session()

    agendamento = (db.query(Agendamento).options(joinedload(Agendamento.horario)).filter_by(user_id=current_user.id, status="ativo").first())

    if not agendamento:
        flash("Você não possui agendamento para cancelar.")
        db.close()
        return redirect(url_for("dashboard"))

    
    agendamento.horario.disponivel = True

    
    agendamento.status = "cancelado"

    db.commit()
    db.close()

    flash("Agendamento cancelado com sucesso!")
    return redirect(url_for("dashboard"))

@agendamento_bp.route("/historico")
@login_required
def historico():
    db = Session()

    historico = (db.query(Agendamento).options(joinedload(Agendamento.horario))  .filter_by(user_id=current_user.id).order_by(Agendamento.criado_em.desc()).all())

    db.close()

    return render_template("historico.html",historico=historico,usuario=current_user)

@agendamento_bp.route('/meu_agendamento')
@login_required
def meu_agendamento():
    db = Session()

    agendamento = (db.query(Agendamento).options(joinedload(Agendamento.horario)).filter_by(user_id=current_user.id, status="ativo").first())

    db.close()

    return render_template('meu_agendamento.html',agendamento=agendamento,usuario=current_user)