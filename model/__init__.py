from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("mysql://root:lozinka@localhost:6306/rezerviranjeUcionica?autocommit=True")
Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()
