from fastapi import APIRouter, status

from ..models.ComercioModel import ComercioRequestModel, ComercioTableModel

router = APIRouter()

@router.post(
    '/new', 
    status_code=status.HTTP_201_CREATED,
    response_model=str,
    summary='Receba uma chave de API para o seu comércio',
    tags=['Comercio', 'Commerce'],
    responses={
        201: {
            'description': 'Uma nova chave API',
            'content': {
                'application/json': {
                    'example': 'inv_admin_dLLvsZHFILBQ3IoD23_Y5R1nQZ41LEI9f-bvVBdJtf0'
                    }
                }
        }
    }
)
def create_comercio(com_data: ComercioRequestModel) -> str:
    # TODO: Check if the comercio doesn't already exist
    obj = ComercioTableModel(com_data)
    apikey = obj.build()
    return apikey
