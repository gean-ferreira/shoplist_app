from fastapi import Request
from .auth_handler import decode_access_token


# Função para obter o usuário atual baseado no token
def get_current_user(request: Request):
    access_token = request.cookies.get("access_token")
    payload = decode_access_token(access_token)
    return int(payload["sub"])
