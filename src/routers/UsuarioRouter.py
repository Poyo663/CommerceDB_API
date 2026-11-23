from fastapi import APIRouter

from src.models.UsuarioModel import UsuarioRequestModel, UsuarioResponseModel, UsuarioTableModel

router = APIRouter()

@router.post('/get')
def get_usuario(userData: UsuarioRequestModel) -> UsuarioResponseModel:
    obj = UsuarioTableModel(userData)
    user = obj.fetch_user()
    return user

@router.post('/new')
def create_usuario(userData: UsuarioRequestModel):
    obj = UsuarioTableModel(userData)
    obj.build()
    return 200

