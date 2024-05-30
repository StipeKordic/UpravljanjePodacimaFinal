from http.client import HTTPException
import utils
from sqlalchemy.orm import Session
from controllers.base_controller import BaseController
from models import User
from repositories.user_repository import UserRepository
from schemas import PasswordChange
from services.result import Result


class UserController(BaseController):
    def __init__(self, db: Session):
        super().__init__(db, UserRepository(User))

    def change_password(self, passwords: PasswordChange, user_id: int):
        try:
            result: Result = self.get_one(user_id)
            if not utils.verify(passwords.old_password, result.value.password):
                raise Exception("Invalid credentials")
            if passwords.password != passwords.confirm_password:
                raise Exception("Passwords do not match")
            passwords.password = utils.hash(passwords.password)
            item = self.default_repo.update(self.db, db_obj=result.value, obj_in=passwords)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)

