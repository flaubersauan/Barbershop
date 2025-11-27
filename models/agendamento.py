from sqlalchemy import DateTime,Integer, ForeignKey
from datetime import datetime
from sqlalchemy.orm import mapped_column
from database.conexao import Base


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = mapped_column(Integer, primary_key=True)

    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    horario_id = mapped_column(ForeignKey("horarios.id"), nullable=False)

    criado_em = mapped_column(DateTime, default=datetime.utcnow)

