import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))   


class Config:
    SECRET_KEY = 'clave_secreta-maquirenthal'


    SQLALCHEMY_DATABASE_URI = (
               'SQLite:///' + 
         os.path.join(BASE_DIR, 'data', 'maquirenthal.db')
    )
sqlalchemy_track_modifications = False
