from sqlalchemy.orm import sessionmaker,DeclarativeBase
from sqlalchemy import create_engine

engine = create_engine('mysql://root:@localhost/barbershop')
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

