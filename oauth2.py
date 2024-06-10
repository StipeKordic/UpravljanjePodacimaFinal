from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
import os
from schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import redis


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
r = redis.Redis(host='redis', port=6379, decode_responses=True)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        if r.get(token) == 'invalid':
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")
        username: str = payload.get("username")
        is_admin: bool = payload.get("is_admin")

        if id is None:
            raise credentials_exception
        token_data = TokenData(user_id=id, username=username, is_admin=is_admin)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)

def invalidate_token(token: str):
    r.set(token, "invalid", ex=int(ACCESS_TOKEN_EXPIRE_MINUTES)*60)

    return {"message": "Token invalidated"}


