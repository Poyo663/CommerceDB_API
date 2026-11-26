import secrets
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field
from sqlalchemy import Connection, text
from fastapi import HTTPException, status

from ..utils.db import connection_established
from ..utils.hash import generate_api_key, hash

class ComercioRequestModel(BaseModel):
    name: str = Field(
            ...,
            min_length=5,
            max_length=255,
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
        api_key_hash = hash(apiKey)

        result = conn.execute(
            text("""
                SELECT id FROM Comercio
                WHERE apikey_crypt = :key
                AND ativo = 1
            """),
            {"key": api_key_hash}
        ).first()

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key inválida ou comércio desativado"
            )

        return result[0]

    @connection_established
    def build(self, conn: Connection):
        conn.execute(text(
            "INSERT INTO Comercio (apikey_crypt, nome_comercio, email) VALUES (:key , :nome , :email)"),
             {"key": hash(self.apikey), "nome": self.name, "email": self.email})
        conn.commit()
        return self.apikey


    @staticmethod
    @connection_established
    def solicitar_exclusao(api_key: str, conn: Connection):
        comercio = conn.execute(
            text("""
                SELECT id, email FROM Comercio
                WHERE apikey_crypt = :key
                AND ativo = 1
            """),
            {"key": hash(api_key)}
        ).first()

        if comercio is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key inválida ou comércio desativado"
            )

        id_comercio = comercio[0]
        email = comercio[1]

        token = secrets.token_urlsafe(32)
        token_hash = hash(token)

        data_expiracao = (
            datetime.now(timezone.utc) + timedelta(minutes=30)
        ).strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            text("""
                UPDATE SolicitacaoExclusao
                SET utilizado = 1
                WHERE id_comercio = :id_comercio
                AND utilizado = 0
            """),
            {"id_comercio": id_comercio}
        )

        conn.execute(
            text("""
                INSERT INTO SolicitacaoExclusao (
                    id_comercio,
                    token_hash,
                    data_expiracao,
                    utilizado
                )
                VALUES (
                    :id_comercio,
                    :token_hash,
                    :data_expiracao,
                    0
                )
            """),
            {
                "id_comercio": id_comercio,
                "token_hash": token_hash,
                "data_expiracao": data_expiracao
            }
        )

        conn.commit()

        return email, token


    @staticmethod
    @connection_established
    def confirmar_exclusao(token: str, conn: Connection):
        token_hash = hash(token)

        agora = datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        solicitacao = conn.execute(
            text("""
                SELECT
                    s.id,
                    s.id_comercio,
                    s.data_expiracao,
                    s.utilizado,
                    c.ativo
                FROM SolicitacaoExclusao AS s
                INNER JOIN Comercio AS c
                    ON s.id_comercio = c.id
                WHERE s.token_hash = :token_hash
            """),
            {"token_hash": token_hash}
        ).first()

        if solicitacao is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de confirmação inválido"
            )

        id_solicitacao = solicitacao[0]
        id_comercio = solicitacao[1]
        data_expiracao = solicitacao[2]
        utilizado = solicitacao[3]
        ativo = solicitacao[4]

        if utilizado == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token já utilizado ou invalidado"
            )

        if data_expiracao <= agora:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de confirmação expirado"
            )

        if ativo == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Comércio já desativado"
            )

        resultado = conn.execute(
            text("""
                UPDATE SolicitacaoExclusao
                SET utilizado = 1
                WHERE id = :id_solicitacao
                AND utilizado = 0
                AND data_expiracao > :agora
            """),
            {
                "id_solicitacao": id_solicitacao,
                "agora": agora
            }
        )

        if resultado.rowcount != 1:
            conn.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido ou indisponível"
            )

        resultado = conn.execute(
            text("""
                UPDATE Comercio
                SET ativo = 0
                WHERE id = :id_comercio
                AND ativo = 1
            """),
            {"id_comercio": id_comercio}
        )

        if resultado.rowcount != 1:
            conn.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Comércio já desativado"
            )

        conn.execute(
            text("""
                UPDATE SolicitacaoExclusao
                SET utilizado = 1
                WHERE id_comercio = :id_comercio
                AND utilizado = 0
            """),
            {"id_comercio": id_comercio}
        )

        conn.commit()

        return {
            "message": "Comércio desativado com sucesso"
        }


class ExclusaoRequestModel(BaseModel):
    api_key: str = Field(
        ...,
        min_length=10,
        max_length=255,
        description="Chave de API do comércio"
    )


class ExclusaoConfirmModel(BaseModel):
    token: str = Field(
        ...,
        min_length=10,
        max_length=255,
        description="Token de confirmação recebido por e-mail"
    )
