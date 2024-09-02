from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "Error na leitura do SECRET_KEY para codificação JWT, verificar arquivo .env"
    )

ALGORITHM = "HS256"


def create_access_token(user_id: str, expires_delta: timedelta = None):
    to_encode = {"sub": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


