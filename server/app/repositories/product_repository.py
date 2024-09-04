""" 
Este módulo contém funções que interagem diretamente com o banco de dados para as operações CRUD relacionadas aos produtos
"""

from app.core.database import database
from app.models.product_models import ProductBaseModel


class ProductRepository:

    async def get_products(self):
        query = "SELECT * FROM shoplist_db.Product;"
        return await database.fetch_all(query)

    async def get_product_by_id(self, product_id: int):
        query = "SELECT * FROM shoplist_db.Product WHERE product_id = :product_id;"
        return await database.fetch_one(query, {"product_id": product_id})

    async def get_product_by_name(self, product_name: str):
        query = "SELECT * FROM shoplist_db.Product WHERE product_name = :product_name"
        return await database.fetch_one(query, {"product_name": product_name})

    async def create_product(self, product: ProductBaseModel):
        query = "INSERT INTO shoplist_db.Product (product_name) VALUES (:product_name);"
        return await database.execute(
            query,
            {"product_name": product.product_name},
        )

    async def update_product(self, product_id: int, product: ProductBaseModel):
        query = "UPDATE shoplist_db.Product SET product_name = :product_name WHERE product_id = :product_id;"
        return await database.execute(
            query, {"product_name": product.product_name, "product_id": product_id}
        )

    async def delete_product(self, product_id: int):
        query = "DELETE FROM shoplist_db.Product WHERE product_id = :product_id;"
        return await database.execute(query, {"product_id": product_id})
