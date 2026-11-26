from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from ..models.ProdutoModel import Produto, ProdutoRequestModel, ProdutoTableModel

router = APIRouter()

@router.get(
    '/{api_key}',
    status_code=status.HTTP_200_OK,
    response_model=list[Produto],
    summary='Lista todos os produtos registrados a um comércio',
    tags=['Produto'],
    responses={
        200: {
            'description': 'A lista de produtos do comércio',
            'content': {
                'application/json': {
                    'example': [{ 'nome': 'Pastel de frango com catupiry', 'preco': 9.99 }, { 'nome': 'Parafuso pequeno', 'preco': 5}]
                    }
                }
        }
    }
)
def get_produtos(
        api_key: Annotated[ 
                str,
                Path(
                    description='A sua chave de API',
                    examples=['inv_admin_dLLvsZHFILBQ3IoD23_Y5R1nQZ41LEI9f-bvVBdJtf0']
            )
    ]
) -> list[Produto]:
    return ProdutoTableModel.fetch_all(api_key)

@router.post(
    '/new', 
    status_code=status.HTTP_201_CREATED,
    response_model=list[Produto],
    summary='Registre novos produtos para o comércio',
    tags=['Produto'],
    responses={
        201: {
            'description': 'A lista de produtos adicionados',
            'content': {
                'application/json': {
                    'example': [{ 'nome': 'Pastel de frango com catupiry', 'preco': 9.99 }, { 'nome': 'Parafuso pequeno', 'preco': 5}]
                    }
                }
        }
    }
)
def create_produto(prod_data: ProdutoRequestModel) -> list[Produto]:
    obj = ProdutoTableModel(prod_data)
    return obj.build()
