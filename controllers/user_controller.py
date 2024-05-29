from sqlalchemy.orm import Session
from controllers.base_controller import BaseController
from models import User
from repositories.user_repository import UserRepository


class UserController(BaseController):
    def __init__(self, db: Session):
        super().__init__(db, UserRepository(User))
