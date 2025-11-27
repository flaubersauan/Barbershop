from sqlalchemy import DateTime, Integer, ForeignKey
from datetime import datetime
from sqlalchemy.orm import mapped_column, relationship
from database.conexao import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = mapped_column(Integer, primary_key=True)

    # 1 usuário → 1 agendamento
    user_id = mapped_column(
        Integer,ForeignKey("users.id"),unique=True,nullable=False)

    # 1 horário → 1 agendamento
    horario_id = mapped_column(
        Integer,ForeignKey("horarios.id"),unique=True,nullable=False)

    criado_em = mapped_column(DateTime, default=datetime.utcnow)
