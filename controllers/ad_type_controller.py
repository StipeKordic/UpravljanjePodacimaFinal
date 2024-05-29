from sqlalchemy.orm import Session
from controllers.base_controller import BaseController
from models import AdType
from repositories.ad_type_repository import AdTypeRepository


class AdTypeController(BaseController):
    def __init__(self, db: Session):
        super().__init__(db, AdTypeRepository(AdType))