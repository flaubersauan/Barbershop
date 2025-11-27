from sqlalchemy import Time, Integer, Date, Boolean
from sqlalchemy.orm import mapped_column, relationship, backref
from database.conexao import Base

class Horario(Base):
    __tablename__ = "horarios"

    id = mapped_column(Integer, primary_key=True)
    data = mapped_column(Date, nullable=False)
    hora = mapped_column(Time, nullable=False)
    disponivel = mapped_column(Boolean, default=True)

    agendamento = relationship("Agendamento",backref=backref("horario"))