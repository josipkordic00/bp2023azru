from sqlalchemy.orm import relationship

from .ucenik import Ucenik
from .evidencija import Evidencija
from .nastavnik import Nastavnik
from .obavijesti import Obavijesti
from .ucionica import Ucionica
from .ustanova import Ustanova
from . import Base
from . import engine


Evidencija.nastavnik = relationship("Nastavnik", back_populates="evidencija")
Evidencija.ustanova = relationship("Ustanova", back_populates="evidencija")
Evidencija.ucionica = relationship("Ucionica", back_populates = "evidencija")
Nastavnik.evidencija = relationship("Evidencija", back_populates="nastavnik")
Ustanova.evidencija = relationship("Evidencija", back_populates="ustanova")
Ucionica.evidencija = relationship("Evidencija", back_populates ="ucionica")
Obavijesti.nastavnik = relationship("Nastavnik", back_populates="obavijesti")
Nastavnik.obavijesti = relationship("Obavijesti", back_populates = "nastavnik")
Ucionica.nastavnik = relationship("Nastavnik", back_populates="ucionica")
Ucionica.ustanova = relationship("Ustanova", back_populates ="ucionica")
Nastavnik.ucionica = relationship("Ucionica", back_populates="nastavnik")
Ustanova.ucionica = relationship("Ucionica", back_populates = "ustanova")


Base.metadata.create_all(engine)