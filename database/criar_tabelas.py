from database.conexao import Base, engine
from models.user import User
from models.horario import Horario
from models.agendamento import Agendamento

Base.metadata.create_all(engine)