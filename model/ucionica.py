from . import Base
from sqlalchemy import *


class Ucionica(Base):
    __tablename__ = "ucionica"
    id = Column(Integer, primary_key=True)
    broj_ucionice = Column(Integer)
    datum_rezervacije = Column(DateTime)
    zauzeto = Column(Boolean)
    nastavnik_id = Column(Integer, ForeignKey('nastavnik.id'))
    ustanova_id = Column(Integer, ForeignKey('ustanova.id'))
   
    

    