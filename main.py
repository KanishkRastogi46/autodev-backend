import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import OAuth2PasswordBearer

from app.routes.users import user_router
from app.routes.auth import router
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
app.include_router(router, prefix="/auth")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers= ["*"],
)

if __name__=="__main__":
    uvicorn.run(app)