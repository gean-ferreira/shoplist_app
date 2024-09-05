from fastapi import APIRouter, Depends

from fastapi import APIRouter, Depends, status
from app.models.error_models import DetailErrorResponse

from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.response_models import BaseResponseModel
from app.models.shopping_list_models import (
    ShoppingListBaseModel,
    ShoppingListInModel,
    ShoppingListOutDataModel,
    ShoppingListOutModel,
    ShoppingListResponseModel,
)
from app.repositories.shopping_list_repository import ShoppingListRepository
from app.services.shopping_list_service import ShoppingListService
from app.security.dependencies import get_current_user

router = APIRouter()
shopping_list_service = ShoppingListService(ShoppingListRepository())


@router.get(
    "/shopping-lists/",
    response_model=ShoppingListResponseModel,
    responses={
        200: {
            "model": ShoppingListResponseModel,
            "description": "Os detalhes das listas de compras, incluindo ID, nome da lista e data na qual foi criada, são retornados na resposta.",
        },
        401: {
            "model": DetailErrorResponse,
            "description": "O error é retornado caso a requisição falhou porque o token de acesso é inválido, expirou ou não foi fornecido.",
        },
    },
    summary="Lista Todas as Listas do Usuário Autenticado",
    description="""
    Retorna todas as listas criada pelo usuário autenticado.
    
    Cada lista é retornada com seu ID, nome e data que foi criada.
    """,
    tags=["Lista de compras"],
)
async def get_shopping_lists(user_id: int = Depends(get_current_user)):
    shopping_lists_records = await shopping_list_service.get_shopping_lists(user_id)
    shopping_lists = [
        ShoppingListBaseModel(**shopping_list)
        for shopping_list in shopping_lists_records
    ]
    return ShoppingListResponseModel(
        message="Listas de compras listadas com sucesso", data=shopping_lists
    )


@router.post(
    "/shopping-lists/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": ShoppingListOutDataModel,
            "description": "Lista de compras criada com sucesso. Retorna os detalhes da nova lista.",
        },
        401: {
            "model": DetailErrorResponse,
            "description": "O error é retornado caso a requisição falhou porque o token de acesso é inválido, expirou ou não foi fornecido.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente, como um nome de lista inválido.",
        },
    },
    summary="Cria uma Nova Lista de compras do Usuário Autenticado",
    description="""
    Registra uma nova lista de compras vinculado ao usuário logado na plataforma.

    Para criar uma lista de compras, é necessário fornecer um nome para a lista.

    Em caso de sucesso, retorna os dados da lista de compras (ID e nome).
    """,
    tags=["Lista de compras"],
)
async def create_shopping_list(
    shopping_list: ShoppingListInModel, user_id: int = Depends(get_current_user)
):
    db_shopping_list = await shopping_list_service.create_shopping_list(
        user_id, shopping_list.list_name
    )
    shopping_list_data = ShoppingListOutModel(
        list_id=db_shopping_list, list_name=shopping_list.list_name
    )
    return ShoppingListOutDataModel(
        message="Listas de compras criada com sucesso", data=shopping_list_data
    )


@router.put(
    "/shopping-lists/{list_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Lista de compras atualizada com sucesso.",
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
            "description": "Erro de validação na entrada de dados.",
        },
    },
    summary="Atualiza Lista de Compras do Usuário Autenticado",
    description="""
    Atualiza a lista de compras do usuário autenticado na plataforma, identificado pelo seu ID único.

    É necessário fornecer um novo nome para a lista.
    """,
    tags=["Lista de compras"],
)
async def update_shopping_list(
    list_id: int,
    shopping_list: ShoppingListInModel,
    user_id: int = Depends(get_current_user),
):
    message = await shopping_list_service.update_shopping_list(
        list_id, shopping_list.list_name, user_id
    )
    return BaseResponseModel(message=message)


@router.delete(
    "/shopping-lists/{list_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Confirmação de que a lista de compras foi excluída com sucesso.",
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
    summary="Exclui Lista de Compras do Usuário Autenticado",
    description="""
    Exclui uma lista de compras específica da plataforma, identificado pelo seu ID único.

    Essa operação é irreversível.
    Uma vez que a lista de compras é excluída, todos os dados associados a essa lista serão permanentemente removidos.
    Utilize essa operação com cuidado.
    """,
    tags=["Lista de compras"],
)
async def delete_shopping_list(
    list_id: int,
    user_id: int = Depends(get_current_user),
):
    message = await shopping_list_service.delete_shopping_list(list_id, user_id)
    return BaseResponseModel(message=message)
