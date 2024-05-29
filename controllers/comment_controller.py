from sqlalchemy.orm import Session
from controllers.base_controller import BaseController
from models import Comment
from repositories.comment_repository import CommentRepository


class CommentController(BaseController):
    def __init__(self, db: Session):
        super().__init__(db, CommentRepository(Comment))
