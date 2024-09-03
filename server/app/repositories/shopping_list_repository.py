""" 
Este módulo contém funções que interagem diretamente com o banco de dados para as operações CRUD relacionadas as listas de compra do usuário
"""

from app.core.database import database


class ShoppingListRepository:

    async def get_shopping_lists(self, user_id: int):
        query = "SELECT list_id, list_name, created_at FROM shoplist_db.ShoppingList WHERE user_id = :user_id;"
        return await database.fetch_all(query, {"user_id": user_id})

    async def get_shopping_list_by_id(self, list_id: int):
        query = "SELECT * FROM shoplist_db.ShoppingList WHERE list_id = :list_id;"
        return await database.fetch_one(query, {"list_id": list_id})

    async def create_shopping_list(self, user_id: int, list_name: str):
        query = "INSERT INTO shoplist_db.ShoppingList (list_name, user_id) VALUES (:list_name, :user_id);"
        return await database.execute(
            query,
            {
                "list_name": list_name,
                "user_id": user_id,
            },
        )

    async def update_shopping_list(self, list_id: int, list_name: str):
        query = "UPDATE shoplist_db.ShoppingList SET list_name = :list_name WHERE list_id = :list_id;"
        return await database.execute(
            query, {"list_name": list_name, "list_id": list_id}
        )

    async def delete_shopping_list(self, list_id: int):
        query = "DELETE FROM shoplist_db.ShoppingList WHERE list_id = :list_id;"
        return await database.execute(query, {"list_id": list_id})
