import os

from dotenv import load_dotenv, dotenv_values
from sqlalchemy import create_engine, text

load_dotenv()

dbEngine = None

def connection_established(func):
    def res():
        if not dbEngine:
            create_engine()
        func(dbEngine.connect())
    return res

def create_engine():
    path = os.getenv("PROJECT_ABS_PATH") + os.getenv("DB_NAME")
    dbUsed = os.getenv("DB_OPTION")
    print(path)
    engine = create_engine(f'{dbUsed}:///{path}', echo=True)
    dbEngine = engine
    """
    Abaixo está código para aprendizado/testes
    """
    dbConnection = engine.connect()
    print(dbConnection.execute(text("select * from Comercio")).all())

create_engine()
