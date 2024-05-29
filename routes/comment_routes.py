from database import get_db
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from schemas import Comment, TokenData, CommentCreate

from controllers.comment_controller import CommentController
from oauth2 import get_current_user
from services.result import Result

comment_router = APIRouter(
    prefix="/comment",
    tags=["Comments"]
)


@comment_router.get("/", response_model=List[Comment])
def get_comments(db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = CommentController(db).get_many()
    return result.items


@comment_router.get("/{comment_id}", response_model=Comment)
def get_comment(comment_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = CommentController(db).get_one(comment_id)
    return result.item


@comment_router.post("/", response_model=Comment)
async def create_comment(comment: Comment, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    comment_data = dict(comment)
    comment_data["user_id"] = user.user_id
    comment_create = CommentCreate(**comment_data)
    result: Result = await CommentController(db).create(comment_create)
    return result.item



@comment_router.put("/{comment_id}", response_model=Comment)
def update_comment(comment_id: int, comment: Comment, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = CommentController(db).update(comment, comment_id)
    return result.item


@comment_router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    result: Result = CommentController(db).delete(comment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
