from . import Base
from sqlalchemy import *



class Ucenik(Base):
    __tablename__ = "ucenik"
    id = Column(Integer, primary_key=True)
    ime = Column(String(50))
    prezime = Column(String(50))
    email = Column(String(50))
    sifra = Column(String(50))
    broj_telefona = Column(Integer)
    prisutnost = Column(Boolean)