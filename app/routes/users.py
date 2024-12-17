from typing import Annotated, Union
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import os
from dotenv import load_dotenv
import random

from app.model import User
from app.schema import UserRegister, ChatResponse, Prompt, ChatError, RegisterResponse, VerifyEmail
from app import get_db
from app.chat import get_response
from app.auth.auth_handler import hash_password, get_current_user

load_dotenv()

conf = ConnectionConfig(
   MAIL_USERNAME=os.getenv("SENDER_EMAIL"),
   MAIL_PASSWORD=os.getenv("SENDER_EMAIL_PASSWORD"),
   MAIL_FROM = os.getenv("SENDER_EMAIL"),
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_FROM_NAME=os.getenv("SENDER_NAME"),
   MAIL_STARTTLS = True,
   MAIL_SSL_TLS = False,
   USE_CREDENTIALS = True,
   VALIDATE_CERTS = True
)

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
        s = "123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        code = ""
        for i in range(12):
            code += random.choice(s)
        new_user = User(fullname=user.fullname, email=user.email, password=hashed_password, verify_code=code)
        db.add(new_user)
        db.commit()
        template = f"""
        <html>
            <body>
                <h1>AutoDev email verification</h1>
                <div>Click <a href="https://autodev-frontend.vercel.app/verify-email/?email={new_user.email}&code={new_user.verify_code}" target"_blank">here</a> to verify</div>
            </body>
        </html>
        """
        message = MessageSchema(
            subject="Email veriication",
            recipients=[new_user.email],
            body=template,
            subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        return RegisterResponse(message=f"Created user {new_user.email}", success= True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@user_router.post("/chat", response_model= Union[ChatResponse, ChatError])
async def chat(prompt: Prompt, req: Request, db: Session= Depends(get_db)):
    if not req.headers["authorization"].split(" ")[1]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = req.headers["authorization"].split(" ")[1]
    await get_current_user(token, db)
        
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
    
    
@user_router.post("/verify-email")
async def verify_email(data: VerifyEmail, db: Annotated[Session, Depends(get_db)]):
    user_exists = db.query(User).filter_by(email=data.email).first()
    if not user_exists:
        raise HTTPException(
            status_code=401,
            detail="User doesn't exists"
        )
    if user_exists.verify_code != data.code:
        raise HTTPException(
            status_code=401,
            detail="Invalid verification code"
        )
    user_exists.is_verified = True
    user_exists.verify_code = ""
    db.commit()
    return {
        "message": "User verification successfull",
        "success": True
    }