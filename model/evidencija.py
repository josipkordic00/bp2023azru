from . import Base
from sqlalchemy import *

class Evidencija(Base):
    __tablename__ = "evidencija"
    id = Column(Integer, primary_key=True)
    ucenici = Column(Text)
    datum = Column(DateTime)
    nastavnik_id = Column(Integer, ForeignKey('nastavnik.id'))
    ustanova_id = Column(Integer, ForeignKey('ustanova.id'))
    ucionica_id = Column(Integer, ForeignKey('ucionica.id'))
    