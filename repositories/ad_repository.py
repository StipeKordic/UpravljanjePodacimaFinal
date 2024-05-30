from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from repositories.base_repository import BaseRepository
from models import Like


class AdRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

    def is_liked(self, session: Session, ad_id: int, user_id:int):
        sql_stmt = select(Like).where(Like.ad_id == ad_id, Like.user_id == user_id)
        result = session.execute(sql_stmt)
        return result.scalars().first()

    def like_ad(self, session: Session, ad_id: int, user_id:int):
        like = Like(ad_id=ad_id, user_id=user_id)
        session.add(like)
        session.commit()
        session.refresh(like)
        return like
