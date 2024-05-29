from sqlalchemy.orm import Session
from controllers.base_controller import BaseController
from models import Ad
from repositories.ad_repository import AdRepository
from services.result import Result


class AdController(BaseController):
    def __init__(self, db: Session):
        super().__init__(db, AdRepository(Ad))

    def like_ad(self, ad_id: int, user_id:int) -> Result:
        liked = self.default_repo.is_liked(self.db, ad_id, user_id)
        try:
            if liked:
                item = self.default_repo.delete(self.db, db_obj=liked)
                return Result.ok(item)
            item = self.default_repo.like_ad(self.db, ad_id, user_id)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)