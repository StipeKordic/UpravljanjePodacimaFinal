from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import oauth2
import utils
from database import get_db
from schemas import UserCreate, UserOut, TokenData
from models import User


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@auth_router.post("/signup", response_model=UserOut)
async def create_user(user: UserCreate = Depends(UserCreate), db: Session = Depends(get_db)):

    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Passwords do not match, please provide matching passwords.")

    user_in_db = db.query(User).filter(User.email == user.email).first()
    if user_in_db:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Email is already in use, please provide different one.")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user_data = {key: value for key, value in (user.model_dump()).items() if key != 'confirm_password'}

    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@auth_router.post("/login")
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    data = {"user_id": str(user.id), "username": user.username, "is_admin": user.is_admin}

    access_token = oauth2.create_access_token(data)


    return {"access_token": access_token, "token_type": "Bearer"}

@auth_router.get("/logout")
def logout_user(token: str = Depends(oauth2.oauth2_scheme)):
    oauth2.invalidate_token(token)
    return {"message": "User logged out successfully!"}
