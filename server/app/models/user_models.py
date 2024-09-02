""" 
Este módulo define os modelos de dados utilizados para representar usuários no sistema
"""

from pydantic import BaseModel


class UserBaseModel(BaseModel):
    username: str


class UserInModel(UserBaseModel):
    password: str
