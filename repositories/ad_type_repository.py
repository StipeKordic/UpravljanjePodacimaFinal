from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from repositories.base_repository import BaseRepository


class AdTypeRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)
