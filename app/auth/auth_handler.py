from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

from app.model import User
from app import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plainPassword, hashedPassword):
    return pwd_context.verify(plainPassword, hashedPassword)


async def authenticate_user(db: Session, email: str, password: str)->dict[str,str] | bool:
    find_user_by_email = db.query(User).filter_by(email=email).first()
    if not find_user_by_email:
        return False
    if not verify_password(password, find_user_by_email.password):
        return False
    if not find_user_by_email.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified"
        )
    return {"email": email, "password": password}


def create_access_token(user_data: dict, expires_delta: timedelta | None= None):
    encoded_data = user_data.copy()
    expiry = None
    if expires_delta:
        expiry = datetime.now(timezone.utc) + expires_delta
    else:
        expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    encoded_data.update({"exp": expiry})
    encoded_jwt = jwt.encode(encoded_data, os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


async def get_current_user(token: str= Depends(oauth2_scheme), db: Session= Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET"), algorithms=os.getenv("ALGORITHM"))
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
        