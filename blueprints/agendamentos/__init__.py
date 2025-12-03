from flask import Blueprint

agendamento_bp = Blueprint('agendamento', __name__, url_prefix='/agendamento', template_folder='templates')

from . import routes