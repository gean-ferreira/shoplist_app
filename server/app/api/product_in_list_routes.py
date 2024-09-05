from fastapi import APIRouter, Depends

from fastapi import APIRouter, Depends, status
from app.models.error_models import DetailErrorResponse

from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.product_in_list_models import (
    ProductInListInModel,
    ProductInListOutDataModel,
    ProductInListOutModel,
    ProductInListResponseModel,
)
from app.models.response_models import BaseResponseModel
from app.repositories.product_in_list_repository import ProductInListRepository
from app.services.product_in_list_service import ProductInListService
from app.security.dependencies import get_current_user

router = APIRouter()
product_in_list_service = ProductInListService(ProductInListRepository())


@router.get(
    "/shopping-lists/{list_id}/products/",
    responses={
        200: {
            "model": ProductInListResponseModel,
            "description": "Os detalhes da lista de compras, ID dos produtos da lista, ID dos produtos, seus preços e quantidades, são retornados na resposta.",
        },
        401: {
            "model": DetailErrorResponse,
            "description": "O error é retornado caso a requisição falhou porque o token de acesso é inválido, expirou ou não foi fornecido.",
        },
        403: {
            "model": DetailErrorResponse,
            "description": "Caso o usuário não tem permissão para modificar esses dados.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que a lista de compras não foi encontrada.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente.",
        },
    },
    summary="Lista Produtos da Lista de Compras do Usuário Autenticado",
    description="""
    Retorna todos os produtos da lista criada pelo usuário autenticado.
    
    Cada lista é retornada com seus produtos e seus repectivos ID, ID dos produtos, quantidade e preço.
    """,
    tags=["Produtos da lista de compras"],
)
async def get_products_in_lists(list_id: int, user_id: int = Depends(get_current_user)):
    product_in_list_records = await product_in_list_service.get_products_in_lists(
        list_id, user_id
    )
    product_in_list = [
        ProductInListOutModel(**product_in_list)
        for product_in_list in product_in_list_records
    ]
    return ProductInListResponseModel(
        message="Listas de compras listadas com sucesso", data=product_in_list
    )


@router.post(
    "/shopping-lists/{list_id}/products/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": BaseResponseModel,
            "description": "Produto adicionado na lista com sucesso. Retorna os detalhes do nova produto na lista.",
        },
        401: {
            "model": DetailErrorResponse,
            "description": "O error é retornado caso a requisição falhou porque o token de acesso é inválido, expirou ou não foi fornecido.",
        },
        403: {
            "model": DetailErrorResponse,
            "description": "Caso o usuário não tem permissão para modificar esses dados.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que a lista de compras ou ID do produto da lista de compras não foi encontrada.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente.",
        },
    },
    summary="Cria um Novo Produto na Lista de compras do Usuário Autenticado",
    description="""
    Registra um novo produto na lista de compras vinculado ao usuário logado na plataforma.

    Para criar um produto, é necessário fornecer quantidade e preço.

    Em caso de sucesso, retorna os dados da lista de compras (ID, quantidade e preço).
    """,
    tags=["Produtos da lista de compras"],
)
async def create_product_in_list(
    list_id: int,
    product_in_list: ProductInListInModel,
    user_id: int = Depends(get_current_user),
):
    message = await product_in_list_service.create_product_in_list(
        list_id, product_in_list, user_id
    )
    return BaseResponseModel(message=message)


@router.put(
    "/shopping-lists/{list_id}/products/{product_in_list_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Produto da lista atualizado com sucesso.",
        },
        401: {
            "model": DetailErrorResponse,
            "description": "O error é retornado caso a requisição falhou porque o token de acesso é inválido, expirou ou não foi fornecido.",
        },
        403: {
            "model": DetailErrorResponse,
            "description": "Caso o usuário não tem permissão para modificar esses dados.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que a lista de compras ou ID do produto da lista de compras não foi encontrada.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados.",
        },
    },
    summary="Atualiza Produto da Lista de Compras do Usuário Autenticado",
    description="""
    Atualiza produto da lista de compras do usuário autenticado na plataforma, identificado pelo seu ID único.

    É necessário fornecer uma nova quantidade ou preço do produto.
    """,
    tags=["Produtos da lista de compras"],
)
async def update_product_in_list(
    list_id: int,
    product_in_list_id: int,
    product_in_list: ProductInListInModel,
    user_id: int = Depends(get_current_user),
):
    message = await product_in_list_service.update_product_in_list(
        list_id, product_in_list_id, product_in_list, user_id
    )
    return BaseResponseModel(message=message)


@router.delete(
    "/shopping-lists/{list_id}/products/{product_in_list_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Confirmação de que o produto da lista de compras foi excluído com sucesso.",
        },
        401: {
            "model": DetailErrorResponse,
            "description": "O error é retornado caso a requisição falhou porque o token de acesso é inválido, expirou ou não foi fornecido.",
        },
        403: {
            "model": DetailErrorResponse,
            "description": "Caso o usuário não tem permissão para modificar esses dados.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que a lista de compras não foi encontrado.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados.",
        },
    },
    summary="Exclui Produto da Lista de Compras do Usuário Autenticado",
    description="""
    Exclui um produto da lista de compras específica do usuário autenticado, identificado pelo seu ID único.

    Essa operação é irreversível.
    Uma vez que o produto da lista de compras é excluído, todos os dados associados a esse produto serão permanentemente removidos.
    Utilize essa operação com cuidado.
    """,
    tags=["Produtos da lista de compras"],
)
async def delete_product_in_list(
    list_id: int,
    product_in_list_id: int,
    user_id: int = Depends(get_current_user),
):
    message = await product_in_list_service.delete_product_in_list(
        list_id, product_in_list_id, user_id
    )
    return BaseResponseModel(message=message)
