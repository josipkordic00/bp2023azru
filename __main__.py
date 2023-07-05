from model import *
from model.relacije import *
from model.cache import region, api

ID = 5
KEY = f'ucenik_{ID}'
pero = region.get(KEY)
print(pero)
if pero is api.NO_VALUE:
    pero = session.query(Ucenik).filter(Ucenik.id==ID).one()
    region.set(KEY, pero)
print(pero.ime + " " + pero.prezime)
