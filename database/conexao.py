from sqlalchemy.orm import session,DeclarativeBase
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:@localhost/barbershop')
Session = session(bind=engine)

class Base(DeclarativeBase):
    pass
    