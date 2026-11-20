from fastapi import APIRouter

from ..models.ComercioModel import ComercioRequestModel, ComercioTableModel

router = APIRouter()

@router.post('/new')
def create_comercio(com_data: ComercioRequestModel):
    # TODO: Check if the comercio doesn't already exist
    obj = ComercioTableModel(com_data)
    apikey = obj.build()
    return apikey
