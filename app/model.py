from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100), nullable=False)
    profile_img = Column(Text(), nullable=True)