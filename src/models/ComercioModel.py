from pydantic import BaseModel, Field
from sqlalchemy import Connection, text

from ..utils.db import connection_established
from ..utils.hash import generate_api_key, hash

class ComercioRequestModel(BaseModel):
    name: str = Field(
            ...,
            min_length=3,
            max_digits=255,
            description='Nome do seu comércio',
            examples=['Ronaldo Lanches', 'Lojas Americanas']
        )
    email: str = Field(
            ...,
            min_length=5,
            max_digits=255,
            description='Email profissional do seu comércio',
            examples=['ronaldolanches123@gmail.com', 'lojasamericanas@gmail.com']
        )

class ComercioTableModel():
    def __init__(self, comercio: ComercioRequestModel):
        self.name = comercio.name
        self.email = comercio.email
        self.apikey = generate_api_key()

    @staticmethod
    @connection_established
    def get_id(apiKey: str, conn: Connection) -> int:
        apiKey = hash(apiKey)
        print(apiKey)
        result = conn.execute(text("""
                  SELECT id FROM Comercio
                  WHERE apikey_crypt = :key
          """), { "key": apiKey }).all()
        return result[0][0]

    @connection_established
    def build(self, conn: Connection):
        conn.execute(text(
            "INSERT INTO Comercio (apikey_crypt, nome_comercio, email) VALUES (:key , :nome , :email)"),
             {"key": hash(self.apikey), "nome": self.name, "email": self.email})
        conn.commit()
        return self.apikey
