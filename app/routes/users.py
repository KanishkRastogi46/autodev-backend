from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.model import User
from app.schema import Users, ChatResponse, Prompt
from . import get_db
from app.chat import get_response

user_router = APIRouter()

@user_router.get('/', response_model=list[Users])
def users(db: Annotated[Session, Depends(get_db)]):
    get_users = db.query(User).all()
    return get_users

@user_router.post("/register")
async def register(user: Users, db: Annotated[Session, Depends(get_db)])->str:
    new_user = User(**dict(user))
    try:
        db.add(new_user)
        db.commit()
        return f"Created user {new_user.email}"
    except Exception as e:
        return str(e)
    
@user_router.post("/chat", response_model=ChatResponse)
async def chat(prompt: Prompt):
    res : ChatResponse = get_response(prompt.prompt)
    return res