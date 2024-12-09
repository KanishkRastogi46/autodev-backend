from typing import Annotated, Union
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.model import User
from app.schema import UserRegister, ChatResponse, Prompt, ChatError, RegisterResponse
from app import get_db
from app.chat import get_response
from app.auth.auth_handler import hash_password

user_router = APIRouter()


@user_router.get('/')
def users(db: Annotated[Session, Depends(get_db)]):
    get_users = db.query(User).all()
    return get_users


@user_router.post("/register")
async def register(user: UserRegister, db: Annotated[Session, Depends(get_db)]):
    try:
        user_exists = db.query(User).filter_by(email=user.email).first()
        if user_exists:
            raise HTTPException(status_code=401, detail="User already exists")
        if user.password != user.confirmPassword:
            raise HTTPException(status_code=401, detail="Passwords don't match")
        hashed_password = hash_password(user.password)
        new_user = User(fullname=user.fullname, email=user.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        return RegisterResponse(message="Created user {new_user.email}", success= True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@user_router.post("/chat", response_model= Union[ChatResponse, ChatError])
async def chat(prompt: Prompt):
    try:
        res = get_response(prompt.prompt)
        return ChatResponse(
            Language=res.get("Language"),
            Code=res.get("Code"),
            Explanation=res.get("Explanation"),
            Note=res.get("Note"),
            success=True
        )
    except HTTPException as e:
        return ChatError(message= str(e), success= False)