from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .shopping_list_routes import router as shopping_list_router
from .product_routes import router as product_router
from .product_in_list_routes import router as product_in_list_router

# Exporta lista com todos os roteadores
routers = [
    auth_router,
    user_router,
    shopping_list_router,
    product_router,
    product_in_list_router,
]
