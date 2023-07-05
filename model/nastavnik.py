from . import Base
from sqlalchemy import *



class Nastavnik(Base):
    __tablename__ = "nastavnik"
    id = Column(Integer, primary_key=True)
    ime = Column(String(50))
    prezime = Column(String(50))
    email = Column(String(50))
    sifra = Column(String(50))
    broj_telefona = Column(Integer)
    qr_code_path = Column(String(50))
    
    

    