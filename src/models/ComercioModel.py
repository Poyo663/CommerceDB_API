from pydantic import BaseModel
from sqlalchemy import Connection, text

from ..utils.db import connection_established
from ..utils.hash import generate_api_key, hash

class ComercioRequestModel(BaseModel):
    name: str 
    email: str

class ComercioTableModel():
    def __init__(self, comercio: ComercioRequestModel):
        self.name = comercio.name
        self.email = comercio.email
        self.apikey = generate_api_key()

    @connection_established
    def build(self, conn: Connection):
        conn.execute(text(
            "INSERT INTO Comercio (apikey_crypt, nome_comercio, email) VALUES (:key , :nome , :email)"),
             {"key": hash(self.apikey), "nome": self.name, "email": self.email})
        conn.commit()
        return self.apikey
