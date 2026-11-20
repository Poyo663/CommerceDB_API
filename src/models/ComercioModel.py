from pydantic import BaseModel
from sqlalchemy import Connection, text

from ..utils.db import connection_established

class ComercioRequestModel(BaseModel):
    name: str 
    email: str

def make_key():
    return "key"

class ComercioTableModel():
    def __init__(self, comercio: ComercioRequestModel):
        self.name = comercio.name
        self.email = comercio.email
        self.apikey = make_key()

    @connection_established
    def build(self, conn: Connection):
        conn.execute(text(
            "INSERT INTO Comercio (apikey_crypt, nome_comercio, email) VALUES (:key , :nome , :email)"),
             {"key": self.apikey, "nome": self.name, "email": self.email})
        conn.commit()
        return self.apikey
