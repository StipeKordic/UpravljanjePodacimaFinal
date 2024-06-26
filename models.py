from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from database import Base
from sqlalchemy import Column, Integer, Text, String, Float, ForeignKey, Boolean, PrimaryKeyConstraint
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))


class AdType(Base):
    __tablename__ = "ad_types"

    id = Column(Integer, primary_key=True)
    ad_type = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)


class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ad_type_id = Column(Integer, ForeignKey("ad_types.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    image_path = Column(String(255))
    category = Column(String(255))

    user = relationship("User", backref=backref("ads", lazy="dynamic"))
    ad_type = relationship("AdType", backref=backref("ads", lazy="dynamic"))
    comments = relationship("Comment", backref=backref("ad", lazy="joined"))
    likes = relationship("Like", backref=backref("ad", lazy="joined"))

    @hybrid_property
    def likes_count(self):
        return len(self.likes)


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ad_id = Column(Integer, ForeignKey("ads.id"), nullable=False)


    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'ad_id'),
    )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ad_id = Column(Integer, ForeignKey("ads.id"), nullable=False)
    comment = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
