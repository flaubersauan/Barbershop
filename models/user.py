from sqlalchemy import String, Integer, and_
from sqlalchemy.orm import mapped_column, relationship, backref
from flask_login import UserMixin
from database.conexao import Base

class User(UserMixin, Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    nome = mapped_column(String(100), nullable=False)
    email = mapped_column(String(120), nullable=False, unique=True)
    senha_hash = mapped_column(String(200), nullable=False)

    agendamento = relationship(
        "Agendamento",
        primaryjoin="and_(User.id == Agendamento.user_id, Agendamento.status == 'ativo')",
        uselist=False,
        lazy="joined",
        backref=backref("cliente")
    )
