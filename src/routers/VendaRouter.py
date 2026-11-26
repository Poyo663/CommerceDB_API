from fastapi import APIRouter

from src.models.VendaModel import VendaRequestModel, VendaTableModel

router = APIRouter()

@router.post('/')
def create_venda(vendaData: VendaRequestModel):
    vendaTableInfo = VendaTableModel(vendaData)
    vendaTableInfo.build()
    return 200
