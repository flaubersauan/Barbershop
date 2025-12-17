from flask_login import login_required, current_user
from database.conexao import Session
from models import Agendamento, Horario
from flask import redirect, flash, url_for
from . import horario_bp

@horario_bp.route("/agendar/<int:horario_id>")
@login_required
def agendar(horario_id):
    db = Session()

    horario = db.get(Horario, horario_id)
    if not horario or not horario.disponivel:
        flash("Horário indisponível!")
        db.close()
        return redirect(url_for("dashboard"))

    if current_user.agendamento:
        flash("Você já possui um horário agendado!", 'error')
        db.close()
        return redirect(url_for("dashboard"))


    for ag in horario.agendamento:
        if ag.status == "ativo":
            flash("Este horário já foi reservado!", 'error')
            db.close()
            return redirect(url_for("dashboard"))

    novo = Agendamento(user_id=current_user.id,horario_id=horario.id)

    horario.disponivel = False

    db.add(novo)
    db.commit()
    db.close()

    flash("Agendamento realizado com sucesso!", 'success')
    return redirect(url_for("dashboard"))