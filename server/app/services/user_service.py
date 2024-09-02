""" 
Este módulo contém a lógica de serviço para operações relacionadas aos usuários
"""

from fastapi import HTTPException, status
from app.models.user_models import UserInModel
from app.repositories.user_repository import UserRepository
from app.security.password_hashing import get_password_hash


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def _verify_username_exists(self, username: str):
        db_user = await self.user_repository.get_user_by_username(username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já cadastrado",
            )
        return db_user

    async def create_user(self, user: UserInModel):
        await self._verify_username_exists(user.username)
        user.password = get_password_hash(user.password)
        await self.user_repository.create_user(user)
        return f"Usuário {user.username} cadastrado com sucesso"
