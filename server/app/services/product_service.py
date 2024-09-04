""" 
Este módulo contém a lógica de serviço para operações relacionadas aos produtos
"""

from fastapi import HTTPException, status
from app.models.product_models import ProductBaseModel, ProductOutModel
from app.repositories.product_repository import ProductRepository
from app.security.dependencies import verify_user_permission


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def _verify_product_exists(self, product_id: int):
        db_product = await self.product_repository.get_product_by_id(product_id)
        if db_product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrada",
            )
        return db_product

    async def _verify_name_exists(self, product_name: str):
        db_product = await self.product_repository.get_product_by_name(product_name)
        if db_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O produto com o nome '{product_name}' já está cadastrado",
            )
        return db_product

    async def get_products(self):
        product_records = await self.product_repository.get_products()
        return product_records

    async def create_product(self, product: ProductBaseModel):
        await self._verify_name_exists(product.product_name)
        db_product = await self.product_repository.create_product(product)
        product_data = ProductOutModel(
            product_id=db_product, product_name=product.product_name
        )
        return product_data

    async def update_product(self, product_id: int, product: ProductBaseModel):
        await self._verify_product_exists(product_id)
        await self._verify_name_exists(product.product_name)
        await self.product_repository.update_product(product_id, product)
        return "Produto atualizado com sucesso"

    async def delete_product(self, product_id: int):
        await self._verify_product_exists(product_id)
        await self.product_repository.delete_product(product_id)
        return "Produto deletado com sucesso"
