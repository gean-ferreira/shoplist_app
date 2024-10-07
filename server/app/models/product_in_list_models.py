""" 
Este módulo define os modelos de dados utilizados para representar os produtos da lista
"""

from typing import List, Literal
from pydantic import BaseModel

from app.models.response_models import ResponseWithDataModel


class ProductInListBaseModel(BaseModel):
    quantity_type: Literal['unit', 'kg']
    quantity: float
    price: float


class ProductInListInModel(ProductInListBaseModel):
    product_id: int


class ProductInListOutModel(ProductInListInModel):
    product_in_list_id: int


#
# Respostas
#
class ProductInListResponseModel(ResponseWithDataModel[List[ProductInListOutModel]]):
    pass


class ProductInListOutDataModel(ResponseWithDataModel[ProductInListOutModel]):
    pass
