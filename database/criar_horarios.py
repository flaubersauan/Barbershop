from datetime import date, time
from database.conexao import Session

# IMPORTANTE: importar TODOS os models!
from models.user import User
from models.horario import Horario
from models.agendamento import Agendamento

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

