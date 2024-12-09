from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta
import os
from dotenv import load_dotenv

from app.schema import LoginForm, LoginResponse, SendUser
from app import get_db
from app.auth.auth_handler import authenticate_user, create_access_token

load_dotenv()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=LoginResponse)
async def login(form_data: LoginForm, db: Annotated[Session, Depends(get_db)], response: Response):
    user_exists = await authenticate_user(db, form_data.email, form_data.password)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user details",
            headers={"WWW-Authenticate": "Bearer"}
        )
    else:
        encoded = create_access_token(user_data={"sub": user_exists.get("email")}, expires_delta=timedelta(minutes=int(os.getenv("EXPIRY_TIME"))))
        response.set_cookie(key="accesstoken", value=encoded, httponly=True)
        return LoginResponse(
            message="Login successfull", 
            user= SendUser(email=user_exists.get("email")), 
            access_token=encoded, 
            token_type="Bearer", 
            success= True
        )