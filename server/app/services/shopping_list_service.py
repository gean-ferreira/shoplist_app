""" 
Este módulo contém a lógica de serviço para operações relacionadas aos usuários
"""

from fastapi import HTTPException, status
from app.models.shopping_list_models import ShoppingListBaseModel
from app.repositories.shopping_list_repository import ShoppingListRepository
from app.security.dependencies import verify_user_permission


class ShoppingListService:
    def __init__(self, shopping_list_repository: ShoppingListRepository):
        self.shopping_list_repository = shopping_list_repository

    async def _verify_shopping_list_exists(self, list_id: int):
        db_shopping_list = await self.shopping_list_repository.get_shopping_list_by_id(
            list_id
        )
        if db_shopping_list is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lista de compras não encontrada",
            )
        return db_shopping_list

    async def get_shopping_lists(self, user_id: int):
        shopping_lists_records = await self.shopping_list_repository.get_shopping_lists(
            user_id
        )

        return shopping_lists_records

    async def create_shopping_list(self, user_id: int, list_name: str):
        db_shopping_list = await self.shopping_list_repository.create_shopping_list(
            user_id, list_name
        )
        print(db_shopping_list)
        return db_shopping_list

    async def update_shopping_list(self, list_id: int, list_name: str, user_id: int):
        db_shopping_list = await self._verify_shopping_list_exists(list_id)
        await verify_user_permission(db_shopping_list.user_id, user_id)
        await self.shopping_list_repository.update_shopping_list(list_id, list_name)
        return "Lista de compras atualizada com sucesso"

    async def delete_shopping_list(self, list_id: int, user_id: int):
        db_shopping_list = await self._verify_shopping_list_exists(list_id)
        await verify_user_permission(db_shopping_list.user_id, user_id)
        await self.shopping_list_repository.delete_shopping_list(list_id)
        return "Lista de compras deletada com sucesso"
