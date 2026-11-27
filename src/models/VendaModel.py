from datetime import datetime
from enum import Enum

from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Connection, text

from src.models.ComercioModel import ComercioTableModel
from src.utils.db import connection_established

class VendaStatus(str, Enum):
    """
    Valores para a venda: \n
    'Pendente': a venda foi registrada e o produto ainda não está sendo preparada,\n
    'Preparando': o produto vendido está sendo preparado,\n
    'A Caminho': o produto está em fase de entrega e ainda não chegou ao destino,\n
    'Entregue': o pedido teve a entrega ao cliente confirmada\n
    """

    PENDING   =  'Pendente'
    PREPARING =  'Preparando'
    SHIPPED   =  'A Caminho'
    DELIVERED =  'Entregue'

class VendaRequestModel(BaseModel):
    comercio_apikey: str = Field(
            ...,
            min_length=10,
            max_length=255,
            description='Chave de API fornecida pela API',
            examples=['inv_admin_dLLvsZHFILBQ3IoD23_Y5R1nQZ41LEI9f-bvVBdJtf0']
        )

    id_item: int = Field(
            ...,
            description='Id do item a ser adicionado',
            examples=[14, 20, 530]
        )
    id_cliente: int | None = Field(
            default=None,
            description='Id do cliente que fez a compra',
            examples=[12345, 54682, 981247]
        )
    status: VendaStatus = Field(default=VendaStatus.PENDING)

class VendaTableModel():
    def __init__(self, v: VendaRequestModel) -> None:
        self.id_comercio = ComercioTableModel.get_id(v.comercio_apikey)
        self.hora_compra = str(datetime.now()).split('.')[0]
        self.id_cliente = v.id_cliente
        self.id_item = v.id_item
        self.status = v.status

    @connection_established
    def build(self, conn: Connection):
        conn.execute(text(
            "INSERT INTO Venda (id_comercio, id_item, id_cliente, hora_compra, status) VALUES (:id_comercio, :id_item, :id_cliente, :hora_compra, :status)"),
                     {"id_comercio": self.id_comercio, "id_item": self.id_item, "id_cliente": self.id_cliente, "hora_compra": self.hora_compra, "status": self.status })
        conn.commit()
        return VendaRequestModel(id_item=self.id_item, id_cliente=self.id_cliente, status=self.status)
