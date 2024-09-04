from fastapi import APIRouter, status
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.models.product_models import (
    ProductBaseModel,
    ProductListResponseModel,
    ProductOutDataModel,
    ProductOutModel,
)
from app.models.error_models import DetailErrorResponse, ErrorResponseModel
from app.models.response_models import BaseResponseModel

router = APIRouter()
product_service = ProductService(ProductRepository())


@router.get(
    "/products/",
    response_model=ProductListResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Lista Todos os Produtos",
    description="""
    Retorna uma lista de todas os produtos disponíveis na plataforma.
    
    Cada produto é retornada com detalhes como ID e nome.
    Ideal para usuários visualizarem as opções de produtos disponíveis.
    """,
    response_description="Uma lista de produtos, incluindo detalhes como ID e nome.",
    tags=["Produtos"],
)
async def get_products():
    product_records = await product_service.get_products()
    products = [ProductOutModel(**product) for product in product_records]
    return ProductListResponseModel(
        message="Produtos listados com sucesso", data=products
    )


@router.post(
    "/products/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": ProductOutDataModel,
            "description": "Produto criada com sucesso. Retorna os detalhes do novo produto.",
        },
        400: {
            "model": DetailErrorResponse,
            "description": "Falha na criação da produto devido à tentativa de uso de um nome já existente.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente, como um nome inválido.",
        },
    },
    summary="Cria um Novo Produto",
    description="""
    Registra um novo produto no sistema.

    Para criar um produto, é necessário fornecer detalhes como nome.

    Em caso de sucesso, retorna os detalhes do produto criada. Se houver dados duplicados, como de um nome já utilizado, um erro será retornado.
    """,
    tags=["Produtos"],
)
async def create_product(product: ProductBaseModel):
    db_product = await product_service.create_product(product)
    return ProductOutDataModel(
        message="Produto cadastrada com sucesso", data=db_product
    )


@router.put(
    "/products/{product_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Produto atualizado com sucesso. Retorna a confirmação da atualização.",
        },
        400: {
            "model": DetailErrorResponse,
            "description": "Falha na atualização devido a dados duplicados, como um nome de produto já existente.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que o produto não foi encontrada.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por dados formatados incorretamente ou faltantes.",
        },
    },
    summary="Atualiza os dados de um produto",
    description="""
    Atualiza detalhes de um produto existente no sistema, identificada pelo seu ID único.

    É necessário fornecer os novos dados do produto que deseja atualizar. Se a produto não for encontrada, um erro será retornado.
    """,
    tags=["Produtos"],
)
async def update_product(product_id: int, product: ProductBaseModel):
    message = await product_service.update_product(product_id, product)
    return BaseResponseModel(message=message)


@router.delete(
    "/products/{user_id}/",
    responses={
        200: {
            "model": BaseResponseModel,
            "description": "Confirmação de que o produto foi excluído com sucesso.",
        },
        404: {
            "model": DetailErrorResponse,
            "description": "Retorna uma mensagem indicando que a produto não foi encontrado.",
        },
        422: {
            "model": ErrorResponseModel,
            "description": "Erro de validação na entrada de dados. Pode ocorrer por tentativas de deletar um produto com um ID inválido.",
        },
    },
    summary="Excluir produto",
    description="""
    Exclui um produto específico do sistema, identificado pelo seu ID único.
    
    Essa operação é irreversível. 
    Uma vez que uma produto é excluído, todos os dados associados a esse produto serão permanentemente removidos. 
    Utilize essa operação com cuidado.
    """,
    tags=["Produtos"],
)
async def delete_product(product_id: int):
    message = await product_service.delete_product(product_id)
    return BaseResponseModel(message=message)
