import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def connection_established(func):
    def res(self, *args, **kwargs):
        return func(self, create_db_engine().connect(), *args, **kwargs)
    return res

def create_db_engine():
    path = os.getenv("PROJECT_ABS_PATH") + os.getenv("DB_NAME")
    dbUsed = os.getenv("DB_OPTION")
    print(path)
    engine = create_engine(f'{dbUsed}:///{path}', echo=True)
    return engine

create_db_engine()
