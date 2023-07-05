from . import Base
from sqlalchemy import *



class Obavijesti(Base):
    __tablename__ = "Obavijesti"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    nastavnik_id = Column(Integer, ForeignKey('nastavnik.id'))
    
    