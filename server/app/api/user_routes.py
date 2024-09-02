from fastapi import APIRouter, status
from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.response_models import BaseResponseModel
from app.models.user_models import UserInModel
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService(UserRepository())


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
