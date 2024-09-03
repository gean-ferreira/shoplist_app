from fastapi import Depends, HTTPException, Request
from .auth_handler import decode_access_token


# Função para obter o usuário atual baseado no token
def get_current_user(request: Request):
    access_token = request.cookies.get("access_token")
    payload = decode_access_token(access_token)
    return int(payload["sub"])


# Função para verificar se um valor específico corresponde ao valor do usuário autenticado
async def verify_user_permission(
    resource_id: int, authenticated_user_id: int = Depends(get_current_user)
):
    print(resource_id, authenticated_user_id)
    # Verifica se o ID autenticado é igual ao ID do recurso
    if authenticated_user_id != resource_id:
        raise HTTPException(
            status_code=403, detail="Você não tem permissão para acessar este recurso"
        )
