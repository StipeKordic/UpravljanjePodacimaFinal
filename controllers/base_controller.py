import os
from typing import List
from uuid import uuid4

import aiofiles

from schemas import QueryFilter
from services.result import Result
from sqlalchemy.orm import Session


class BaseController:
    def __init__(self, db: Session, repository):
        self.db = db
        self.default_repo = repository

    def get_many(self, query_params=None, relation_attribute_name: List[str] = None) -> Result:
        try:
            filters: List[QueryFilter] = self._pack_filters(query_params) if query_params else None
            items = self.default_repo.get_all(self.db, relation_attribute_name, filters)

            return Result.ok(items)
        except Exception as ex:
            print(ex)
            return Result.fail(ex)

    def _pack_filters(self, query_params) -> List[QueryFilter]:
        filters = []
        for query_param in query_params:
            if query_param[1]:
                filters.append(QueryFilter(field=query_params.get_fields[query_param[0]],
                                           operator=query_params.get_operators[query_param[0]],
                                           value=query_param[1]))
        return filters

    def get_one(self, _id: int) -> Result:
        try:
            item = self.default_repo.get(self.db, _id)
            if not item:
                raise Exception("Not found")
            return Result.ok(item)
        except Exception as ex:
            print(ex)
            return Result.fail(ex)

    async def create(self, item_in, image=None) -> Result:
        try:
            if image:
                dir_path = "./static/images/"
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                image_filename = f"{uuid4()}{image.filename}"
                image_path = os.path.join(dir_path, image_filename)
                async with aiofiles.open(image_path, 'wb') as out_file:
                    content = await image.read()
                    await out_file.write(content)
                item_in.image_path = image_path
            item = self.default_repo.create(self.db, item_in)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)

    def update(self, item_in, item_id: int) -> Result:
        result: Result = self.get_one(item_id)
        if result.failure:
            return result
        try:
            item = self.default_repo.update(self.db, db_obj=result.value, obj_in=item_in)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)


    def delete(self, item_id: int) -> Result:
        result: Result = self.get_one(item_id)
        if result.failure:
            return result
        try:
            item = self.default_repo.delete(self.db, db_obj=result.value)
            return Result.ok(item)
        except Exception as ex:
            return Result.fail(ex)