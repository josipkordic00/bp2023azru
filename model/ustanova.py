from . import Base
from sqlalchemy import *


class Ustanova(Base):
    __tablename__ = "ustanova"
    id = Column(Integer, primary_key=True)
    naziv = Column(String(50))
    adresa = Column(String(50))
    
