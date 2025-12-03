from flask import Blueprint

horario_bp = Blueprint('horario', __name__, url_prefix='/horario', template_folder='templates')

from . import routes