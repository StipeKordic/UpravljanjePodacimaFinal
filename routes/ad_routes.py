from database import get_db
from fastapi import APIRouter, Depends, status, Response, File, UploadFile, Form
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from schemas import Ad, TokenData, AdOut, AdCreate
import aiofiles
from controllers.ad_controller import AdController
from oauth2 import get_current_user
from services.result import Result
from uuid import uuid4

ad_router = APIRouter(
    prefix="/ad",
    tags=["Ad"]
)


@ad_router.get("/", response_model=List[AdOut])
def get_ads(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = AdController(db).get_many()
    return result.items


@ad_router.get("/{ad_id}", response_model=AdOut)
def get_ad(ad_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = AdController(db).get_one(ad_id)
    return result.item


@ad_router.post("/", response_model=AdOut)
async def create_ad(ad: Ad, image: UploadFile = File(...), db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    ad_data = dict(ad)
    ad_data["user_id"] = user.user_id
    ad_create = AdCreate(**ad_data)
    result: Result = await AdController(db).create(ad_create, image)
    return result.item



@ad_router.put("/{ad_id}", response_model=AdOut)
def update_ad(ad_id: int, ad: Ad, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = AdController(db).update(ad, ad_id)
    return result.item



@ad_router.delete("/{ad_id}")
def delete_ad(ad_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = AdController(db).delete(ad_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ad_router.post("/like/{ad_id}")
def like_ad(ad_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = AdController(db).like_ad(ad_id, user.user_id)
    return result.item
