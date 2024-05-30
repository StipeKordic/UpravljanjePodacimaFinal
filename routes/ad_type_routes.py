from database import get_db
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from schemas import AdType, TokenData

from controllers.ad_type_controller import AdTypeController
from oauth2 import get_current_user
from services.result import Result

ad_type_router = APIRouter(
    prefix="/ad_type",
    tags=["Ad Type"]
)


@ad_type_router.get("/", response_model=List[AdType])
def get_ad_types(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = AdTypeController(db).get_many()
    return result.items


@ad_type_router.get("/{ad_type_id}", response_model=AdType)
def get_ad_type(ad_type_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = AdTypeController(db).get_one(ad_type_id)
    return result.item


@ad_type_router.post("/", response_model=AdType)
async def create_ad_type(ad_type: AdType = Depends(AdType), db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    if user.is_admin:
        result: Result = await AdTypeController(db).create(ad_type)
        return result.item
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@ad_type_router.put("/{ad_type_id}", response_model=AdType)
def update_ad_type(ad_type_id: int, ad_type: AdType = Depends(AdType), db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    if user.is_admin:
        result: Result = AdTypeController(db).update(ad_type, ad_type_id)
        return result.item
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@ad_type_router.delete("/{ad_type_id}")
def delete_ad_type(ad_type_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    if user.is_admin:
        result: Result = AdTypeController(db).delete(ad_type_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")