from fastapi import APIRouter, Depends, status
from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.response_models import BaseResponseModel
from app.models.user_models import UserBaseModel, UserInModel, UserOutDataModel
from app.repositories.user_repository import UserRepository
from app.security.dependencies import get_current_user
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService(UserRepository())


@router.get(
    "/users/",
    responses={
        200: {
            "model": UserOutDataModel,
            "description": "Os detalhes do usuário, incluindo nome de usuário, são retornados na resposta.",
        },
        401: {
            "model": DetailErrorResponse,
            "description": "O error é retornado caso a requisição falhou porque o token de acesso é inválido, expirou ou não foi fornecido.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que o usuário com o ID especificado não foi encontrado no sistema.",
        },
    },
    summary="Busca Dados do Usuário",
    description="""
    Busca um usuário específico pela sua identificação única (ID).

    Esta operação requer que o usuário esteja autenticado e tenha permissão para acessar seus próprios dados. Retorna os dados do usuário, incluindo nome de usuário, caso encontrado. Em caso de erros de autenticação ou permissão, retorna 401 ou 403, respectivamente. Se o usuário não for encontrado, retorna um erro 404.
    """,
    tags=["Usuários"],
)
async def read_user_data(user_id: int = Depends(get_current_user)):
    db_user = await user_service.get_user_by_id(user_id)
    user_data = UserBaseModel(**db_user)
    return UserOutDataModel(
        message="Dados do usuário encontrados com sucesso", data=user_data
    )


@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": BaseResponseModel,
            "description": "Usuário criado com sucesso. Retorna uma mensagem de sucesso.",
        },
        400: {
            "model": DetailErrorResponse,
            "description": "Falha na criação do usuário devido à tentativa de uso de um username já existente.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente.",
        },
    },
    summary="Cria um Novo Usuário",
    description="""
    Registra um novo usuário na plataforma. 

    Para criar um usuário, é necessário fornecer um nome de usuário e uma senha. A senha fornecida será criptografada antes de ser armazenada.

    Em caso de sucesso, retorna uma mensagem de sucesso. Se o nome de usuário já estiver em uso, um erro será retornado.
    """,
    tags=["Usuários"],
)
async def create_user(user: UserInModel):
    message = await user_service.create_user(user)
    return BaseResponseModel(message=message)
