from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from schemas import QueryFilter


class BaseRepository:
    def __init__(self, model):
        self.class_model = model

    def get_all(self, session: Session, relation_attribute_name: List[str] = None, filters: List[QueryFilter] = None):

        sql_stmt = select(self.class_model)
        if filters:
            sql_stmt = self._append_filters(sql_stmt, filters)
        if relation_attribute_name:
            for attribute in relation_attribute_name:
                relation_attribute = getattr(self.class_model, attribute, None)
                sql_stmt = sql_stmt.options(selectinload(relation_attribute))

        result = session.execute(sql_stmt)

        return result.scalars().all()

    def _append_filters(self, sql_stmt, filters):
        for query_filter in filters:
            field = getattr(self.class_model, query_filter.field)

            if query_filter.operator == "eq":
                sql_stmt = sql_stmt.filter(field == query_filter.value)
            elif query_filter.operator == "ge":
                sql_stmt = sql_stmt.filter(field >= query_filter.value)
            elif query_filter.operator == "le":
                sql_stmt = sql_stmt.filter(field <= query_filter.value)
            elif query_filter.operator == "like":
                sql_stmt = sql_stmt.filter(field.ilike(f'{query_filter.value}%'))
        return sql_stmt

    def get(self, session: Session, _id: int):
        sql_stmt = select(self.class_model).where(self.class_model.id == _id)
        result = session.execute(sql_stmt)
        return result.scalars().first()

    def create(self, session, obj_in):
        obj_in_data = dict(obj_in)
        db_obj = self.class_model(**obj_in_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(self, session: Session, db_obj, obj_in):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj


    def delete(self, session, db_obj):
        session.delete(db_obj)
        session.commit()
        return db_obj