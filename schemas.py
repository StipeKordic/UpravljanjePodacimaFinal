from fastapi import Form
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, Tuple, Union
from datetime import datetime
from enum import Enum


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


class QueryFilter(BaseModel):
    field: str
    operator: str
    value: Any

    def to_touple(self) -> Tuple[str, str, Any]:
        return self.field, self.operator, self.value


@form_body
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


@form_body
class PasswordChange(BaseModel):
    old_password: str
    password: str
    confirm_password: str


@form_body
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "user1",
                    "email": "user1@gmail.com",
                    "password": "12345678",
                    "confirm_password": "12345678",
                }
            ]
        }
    }


class UserOut(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool
    created_at: datetime


class AdCategoryEnum(str, Enum):
    TECHNOLOGY = "Technology"
    MAKEUP = "Makeup"
    STYLE = "Style"
    FASHION = "Fashion"
    AUTOMOBILES = "Automobiles"
    HEALTH = "Health"
    FITNESS = "Fitness"
    FOOD = "Food"
    TRAVEL = "Travel"
    EDUCATION = "Education"
    FINANCE = "Finance"
    REAL_ESTATE = "Real Estate"
    ENTERTAINMENT = "Entertainment"
    SPORTS = "Sports"
    BOOKS = "Books"
    MUSIC = "Music"
    MOVIES = "Movies"
    GAMING = "Gaming"
    HOME_DECOR = "Home Decor"
    PETS = "Pets"


@form_body
class Ad(BaseModel):
    title: str
    ad_type_id: int
    category: AdCategoryEnum

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Ad Title",
                    "ad_type_id": 1,
                    "category": "Category"
                }
            ]
        }
    }


class AdOut(Ad):
    id: int
    created_at: datetime
    image_path: str
    user: UserOut
    ad_type: AdType
    likes_count: int


class AdCreate(Ad):
    user_id: int
    image_path: str = None


@form_body
class Comment(BaseModel):
    comment: str
    ad_id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "comment": "This is a comment",
                    "ad_id": 2
                }
            ]
        }
    }


class CommentCreate(Comment):
    user_id: int
