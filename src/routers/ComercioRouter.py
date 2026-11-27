import logging

from fastapi import APIRouter, HTTPException, status

from ..models.ComercioModel import (
    ComercioRequestModel,
    ComercioTableModel,
    ExclusaoRequestModel,
    ExclusaoConfirmModel
)

from ..utils.email import enviar_email_exclusao

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    '/new', 
    status_code=status.HTTP_201_CREATED,
    response_model=str,
    summary='Receba uma chave de API para o seu comércio',
    tags=['Comercio'],
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


@router.post(
    "/unsubscribe/request",
    status_code=status.HTTP_200_OK,
    summary="Solicitar exclusão do comércio",
    tags=["Comercio"]
)
def solicitar_exclusao(dados: ExclusaoRequestModel):

    email, token = ComercioTableModel.solicitar_exclusao(
        dados.api_key
    )

    try:
        enviar_email_exclusao(email, token)

    except Exception:
        logger.error(
            "Falha no serviço de envio de confirmação"
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Não foi possível enviar a confirmação"
        )

    return {
        "message": "Solicitação de exclusão registrada"
    }


@router.post(
    "/unsubscribe/confirm",
    status_code=status.HTTP_200_OK,
    summary="Confirmar exclusão do comércio",
    tags=["Comercio"]
)
def confirmar_exclusao(dados: ExclusaoConfirmModel):

    return ComercioTableModel.confirmar_exclusao(
        dados.token
    )
