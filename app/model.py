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
    is_verified = Column(Boolean, default=False)
    verify_code = Column(String(12), nullable=False)
    chats = relationship("Chat", back_populates="users")
    
class Chat(Base):
    __tablename__= "chats"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text())
    response = Column(Text())
    user_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="chats")