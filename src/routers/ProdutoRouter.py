from fastapi import APIRouter

from ..models.ProdutoModel import Produto, ProdutoRequestModel, ProdutoTableModel

router = APIRouter()

@router.get('/{api_key}')
def get_produtos(api_key: str) -> list[Produto]:
    return ProdutoTableModel.fetch_all(api_key)

@router.post('/new')
def create_produto(prod_data: ProdutoRequestModel):
    obj = ProdutoTableModel(prod_data)
    print(obj.build())
    return 200

