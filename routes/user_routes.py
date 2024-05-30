from database import get_db
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from schemas import UserOut, TokenData, PasswordChange

from controllers.user_controller import UserController
from oauth2 import get_current_user
from services.result import Result

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    if user.is_admin:
        result: Result = UserController(db).get_many()
        return result.items
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@user_router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = UserController(db).get_one(user_id)
    return result.item


@user_router.put("/", response_model=UserOut)
def update_user(password_new: PasswordChange = Depends(PasswordChange), db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    if user.is_admin:
        result: Result = UserController(db).change_password(password_new, user.user_id)
        return result.item
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    if user.is_admin and user.user_id != user_id:
        result: Result = UserController(db).delete(user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")