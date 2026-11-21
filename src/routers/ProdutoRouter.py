from fastapi import APIRouter

from ..models.ProdutoModel import Produto, ProdutoRequestModel, ProdutoTableModel

router = APIRouter()

@router.post('/new')
def create_produto(prod_data: ProdutoRequestModel):
    obj = ProdutoTableModel(prod_data)
    print(obj.build())
    return 200

