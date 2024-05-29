from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, Tuple, Union
from datetime import datetime


class QueryFilter(BaseModel):
    field: str
    operator: str
    value: Any

    def to_touple(self) -> Tuple[str, str, Any]:
        return self.field, self.operator, self.value


class AdType(BaseModel):
    ad_type: str
    description: str
    price: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ad_type": "Banner",
                    "description": "Banner ads can be static or dynamic ads that are strategically positioned on a"
                                   " website to capture consumers’ attention. Through banner advertising, brands can "
                                   "promote their brand as well as encourage viewers to visit the brand's website.",
                    "price": 99.99

                }
            ]
        }
    }


class TokenData(BaseModel):
    user_id: int
    username: str
    is_admin: bool


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    is_admin: bool = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "user1",
                    "email": "user1@gmail.com",
                    "password": "12345678",
                    "confirm_password": "12345678",
                    "is_admin": False,
                }
            ]
        }
    }


class UserOut(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool
    created_at: datetime


class Ad(BaseModel):
    title: str
    user_id: int
    ad_type_id: int
    category: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Ad Title",
                    "user_id": 1,
                    "ad_type_id": 1,
                    "category": "Category"
                }
            ]
        }
    }


