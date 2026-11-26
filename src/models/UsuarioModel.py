from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Connection, text

from ..utils.db import connection_established
from ..utils.hash import hash

class UsuarioRequestModel(BaseModel):
    nome: str | None = None
    email: str
    senha: str

class UsuarioResponseModel(BaseModel):
    id: int
    nome: str
    email: str

class UsuarioTableModel():
    def __init__(self, usuario: UsuarioRequestModel):
        self.nome = usuario.nome
        self.email = usuario.email
        self.senha = hash(usuario.senha)

    @connection_established
    def fetch_user(self, conn: Connection):
        something = conn.execute(
                text(
                    """
                    SELECT * FROM Usuario  
                    WHERE email = :email
                    AND senha_crypt = :senha
                    """
                    ), { "email": self.email, "senha": self.senha }
        ).all()
        if len(something) < 1:
            raise HTTPException(404, detail="Usuário não existe ou email ou senha estão incorretos")
        return UsuarioResponseModel(id=something[0][0], nome=something[0][1] ,email=something[0][2])

    @connection_established
    def build(self, conn: Connection):
        if self.nome is None:
            raise HTTPException(400, detail="Campo 'nome' é obrigatório")

        conn.execute(text(
            "INSERT INTO Usuario (nome_usuario, email, senha_crypt) VALUES (:nome , :email, :senha)"),
             {"nome": self.nome, "email": self.email, "senha": self.senha })
        conn.commit()
