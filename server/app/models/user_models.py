""" 
Este módulo define os modelos de dados utilizados para representar usuários no sistema
"""

from pydantic import BaseModel
from app.models.response_models import ResponseWithDataModel


class UserBaseModel(BaseModel):
    username: str


class UserInModel(UserBaseModel):
    password: str


class UserOutDataModel(ResponseWithDataModel[UserBaseModel]):
    pass
