""" 
Este módulo define os modelos de dados utilizados para representar as listas de compra no sistema
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.models.response_models import ResponseWithDataModel


class ShoppingListBaseModel(BaseModel):
    list_id: int
    list_name: str
    created_at: datetime


class ShoppingListInModel(BaseModel):
    list_name: str


class ShoppingListOutModel(BaseModel):
    list_id: int
    list_name: str


#
# Respostas
#
class ShoppingListResponseModel(ResponseWithDataModel[List[ShoppingListBaseModel]]):
    pass


class ShoppingListOutDataModel(ResponseWithDataModel[ShoppingListOutModel]):
    pass
