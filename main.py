import uvicorn

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

from app.routes.users import user_router
from app.model import User
from app.db import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


app = FastAPI()
app.include_router(user_router, prefix="/users")

if __name__=="__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 8080, reload = True)