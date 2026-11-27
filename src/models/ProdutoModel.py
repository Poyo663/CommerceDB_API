from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import Connection, text
from .ComercioModel import ComercioTableModel

from ..utils.db import connection_established
from ..utils.hash import hash

class Produto(BaseModel):
    nome: str = Field(
            ...,
            min_length=2,
            max_length=255,
            description='Nome do produto',
            examples=['Pastel de frango com catupiry', 'Parafuso pequeno']
        )
    preco: float = Field(
            ...,
            gt=0,
            description='Preço do produto',
            examples=[9.99, 5]
        )

class ProdutoRequestModel(BaseModel):
    api_key: str = Field(
            ...,
            min_length=10,
            max_length=255,
            description='Chave de API fornecida pela API',
            examples=['inv_admin_dLLvsZHFILBQ3IoD23_Y5R1nQZ41LEI9f-bvVBdJtf0']
        )
    produtos: list[Produto] = Field(
            ...,
            min_length=0,
            description='Lista de produtos a se adicionar',
            examples=[[{ 'nome': 'Pastel de frango com catupiry', 'preco': 9.99 }, { 'nome': 'Parafuso pequeno', 'preco': 5}]]
        )

class ProdutoTableModel():
    
    @staticmethod
    @connection_established
    def fetch_all(api_key: str, conn: Connection) -> list[Produto]:
        comercio_id = ComercioTableModel.get_id(api_key)

        produtos = conn.execute(
            text("""
                SELECT p.id, p.nome_item, p.preco
                FROM Produto AS p
                INNER JOIN Comercio AS c
                    ON c.id = p.id_comercio
                WHERE c.id = :id_comercio
                AND c.ativo = 1
            """),
            {"id_comercio": comercio_id}
        ).all()

        res = []

        for p in produtos:
            res.append(
                Produto(
                    nome=p[1],
                    preco=p[2]
                )
            )

        return res

    
    @connection_established
    def build(self, conn: Connection) -> list[Produto]:
        commerceId = ComercioTableModel.get_id(self.api_key)

        prodObjs = []

        for prod in self.produtos:
            prodObjs.append({
                "id_comercio": commerceId,
                "nome_item": prod.nome,
                "preco": prod.preco
            })

        if prodObjs:
            conn.execute(
                text("""
                    INSERT INTO Produto (
                        id_comercio,
                        nome_item,
                        preco
                    )
                    VALUES (
                        :id_comercio,
                        :nome_item,
                        :preco
                    )
                """),
                prodObjs
            )

            conn.commit()

        return self.produtos
