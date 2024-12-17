from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta
import os
from dotenv import load_dotenv

from app.schema import LoginForm, LoginResponse, SendUser
from app import get_db
from app.auth.auth_handler import authenticate_user, create_access_token, get_current_user

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
        response.set_cookie(key="accesstoken", value=encoded, httponly=True, domain="https://autodev-frontend.vercel.app")
        return LoginResponse(
            message="Login successfull", 
            user= SendUser(email=user_exists.get("email")), 
            access_token=encoded, 
            token_type="Bearer", 
            success= True
        )
        
        
@router.get("/", response_model=SendUser)
async def protected_route(req: Request, db: Session = Depends(get_db)):
    # print(req.headers.get("authorization"))
    if req.cookies.get("accesstoken") is not None:
        token = req.cookies.get("accesstoken")
        user = await get_current_user(token, db)
        # print(user)
        return SendUser(
            email= user.email,
            profile= user.profile_img
        )
        
    if req.headers.get("authorization") is not None:
        token = req.headers.get("authorization").split(" ")[1]
        user = await get_current_user(token, db)
        # print(user.email, user.profile_img)
        return SendUser(
            email= user.email,
            profile= user.profile_img
        )
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user details",
            headers={"WWW-Authenticate": "Bearer"}
        )