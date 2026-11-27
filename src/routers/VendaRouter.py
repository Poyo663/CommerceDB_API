from fastapi import APIRouter, status

from src.models.VendaModel import VendaRequestModel, VendaTableModel

router = APIRouter()

@router.post(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=VendaRequestModel,
    summary='Registra nova venda em comércio com comercio_apikey',
    tags=['Venda'],
    responses={
        200: {
            'description': 'A venda que foi registrada',
            'content': {
                'application/json': {
                    'example': { "id_item": 14, "id_cliente": 12345, "status": "Pendente" }
                    }
                }
            }
        }
)
def create_venda(vendaData: VendaRequestModel) -> VendaRequestModel:
    vendaTableInfo = VendaTableModel(vendaData)
    return vendaTableInfo.build()
