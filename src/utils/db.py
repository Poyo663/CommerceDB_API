import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def connection_established(func):
    def res(self, *args, **kwargs):
        with create_db_engine().connect() as conn:
            return func(self, conn, *args, **kwargs)
    return res


def create_db_engine():
    path = os.getenv("PROJECT_ABS_PATH") + os.getenv("DB_NAME")
    dbUsed = os.getenv("DB_OPTION")
    print(path)
    engine = create_engine(f'{dbUsed}:///{path}', echo=False)
    return engine

create_db_engine()
