""" 
Este módulo contém a lógica de serviço para operações relacionadas aos produtos de uma listas de compras
"""

from fastapi import HTTPException, status
from app.models.product_in_list_models import ProductInListInModel
from app.repositories.product_in_list_repository import ProductInListRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.shopping_list_repository import ShoppingListRepository
from app.security.dependencies import verify_user_permission
from app.services.product_service import ProductService
from app.services.shopping_list_service import ShoppingListService

shopping_list_service = ShoppingListService(ShoppingListRepository())
product_service = ProductService(ProductRepository())


class ProductInListService:
    def __init__(self, product_in_list_repository: ProductInListRepository):
        self.product_in_list_repository = product_in_list_repository

    async def get_products_in_lists(self, list_id: int, user_id: int):
        db_shopping_list = await shopping_list_service._verify_shopping_list_exists(
            list_id
        )
        await verify_user_permission(db_shopping_list.user_id, user_id)
        product_in_lists_records = (
            await self.product_in_list_repository.get_products_in_list(list_id)
        )
        return product_in_lists_records

    async def _verify_product_in_list(self, product_in_list_id: int):
        db_product_in_list = (
            await self.product_in_list_repository.get_product_in_list_by_id(
                product_in_list_id
            )
        )
        if db_product_in_list is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não foi encontrado na lista",
            )
        return db_product_in_list

    async def create_product_in_list(
        self, list_id: int, product_in_list: ProductInListInModel, user_id: int
    ):
        db_shopping_list = await shopping_list_service._verify_shopping_list_exists(
            list_id
        )
        await product_service._verify_product_exists(product_in_list.product_id)
        await verify_user_permission(db_shopping_list.user_id, user_id)
        await self.product_in_list_repository.create_product_in_list(
            list_id, product_in_list
        )
        return "Produto adicionado na lista com sucesso"

    async def update_product_in_list(
        self,
        list_id: int,
        product_in_list_id: int,
        product_in_list: ProductInListInModel,
        user_id: int,
    ):
        db_shopping_list = await shopping_list_service._verify_shopping_list_exists(
            list_id
        )
        await self._verify_product_in_list(product_in_list_id)
        await product_service._verify_product_exists(product_in_list.product_id)
        await verify_user_permission(db_shopping_list.user_id, user_id)
        await self.product_in_list_repository.update_product_in_list(
            list_id, product_in_list_id, product_in_list
        )
        return "Produto da lista atualizado com sucesso"

    async def delete_product_in_list(
        self, list_id: int, product_in_list_id: int, user_id: int
    ):
        db_shopping_list = await shopping_list_service._verify_shopping_list_exists(
            list_id
        )
        await self._verify_product_in_list(product_in_list_id)
        await verify_user_permission(db_shopping_list.user_id, user_id)
        await self.product_in_list_repository.delete_product_in_list(
            list_id, product_in_list_id
        )
        return "Lista de compras deletada com sucesso"
