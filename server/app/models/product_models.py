""" 
Este módulo define os modelos de dados utilizados para representar os produtos no sistema
"""

from typing import List
from pydantic import BaseModel

from app.models.response_models import ResponseWithDataModel


class ProductBaseModel(BaseModel):
    product_name: str


class ProductOutModel(ProductBaseModel):
    product_id: int


#
# Respostas
#
class ProductListResponseModel(ResponseWithDataModel[List[ProductOutModel]]):
    pass


class ProductOutDataModel(ResponseWithDataModel[ProductOutModel]):
    pass
