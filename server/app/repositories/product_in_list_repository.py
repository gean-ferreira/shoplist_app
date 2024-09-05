""" 
Este módulo contém funções que interagem diretamente com o banco de dados para as operações relacionadas aos produtos de uma lista
"""

from app.core.database import database
from app.models.product_in_list_models import ProductInListInModel


class ProductInListRepository:

    async def get_products_in_list(self, list_id: int):
        query = "SELECT pil.product_in_list_id, pil.quantity, pil.price, pil.product_id FROM shoplist_db.ProductInList pil JOIN Product p ON pil.product_id = p.product_id WHERE pil.list_id = :list_id;"
        return await database.fetch_all(query, {"list_id": list_id})

    async def get_product_in_list_by_id(self, product_in_list_id: int):
        query = "SELECT * FROM shoplist_db.ProductInList WHERE product_in_list_id = :product_in_list_id;"
        return await database.fetch_one(
            query, {"product_in_list_id": product_in_list_id}
        )

    async def create_product_in_list(
        self, list_id: int, product_in_list: ProductInListInModel
    ):
        query = "INSERT INTO shoplist_db.ProductInList (list_id, product_id, quantity, price) VALUES (:list_id, :product_id, :quantity, :price);"
        return await database.execute(
            query,
            {
                "list_id": list_id,
                "product_id": product_in_list.product_id,
                "quantity": product_in_list.quantity,
                "price": product_in_list.price,
            },
        )

    async def update_product_in_list(
        self,
        list_id: int,
        product_in_list_id: int,
        product_in_list: ProductInListInModel,
    ):
        query = "UPDATE shoplist_db.ProductInList SET product_id = :product_id, quantity = :quantity, price = :price WHERE list_id = :list_id AND product_in_list_id = :product_in_list_id;"
        return await database.execute(
            query,
            {
                "list_id": list_id,
                "product_id": product_in_list.product_id,
                "product_in_list_id": product_in_list_id,
                "quantity": product_in_list.quantity,
                "price": product_in_list.price,
            },
        )

    async def delete_product_in_list(self, list_id: int, product_in_list_id: int):
        query = "DELETE FROM shoplist_db.ProductInList WHERE list_id = :list_id AND product_in_list_id = :product_in_list_id;"
        return await database.execute(
            query,
            {
                "list_id": list_id,
                "product_in_list_id": product_in_list_id,
            },
        )
