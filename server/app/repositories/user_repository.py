""" 
Este módulo contém funções que interagem diretamente com o banco de dados para as operações CRUD relacionadas aos usuários
"""

from app.core.database import database
from app.models.user_models import UserInModel


class UserRepository:

    async def get_user_by_username(self, username: str):
        query = "SELECT * FROM shoplist_db.User WHERE username = :username"
        return await database.fetch_one(query, {"username": username})

    async def create_user(self, user: UserInModel):
        query = "INSERT INTO shoplist_db.User (username, password) VALUES (:username, :password);"
        return await database.execute(
            query,
            {
                "username": user.username,
                "password": user.password,
            },
        )
