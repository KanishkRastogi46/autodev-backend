import uvicorn

from fastapi import Depends, FastAPI, Request, UploadFile, status, HTTPException
# from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import google.generativeai as genai
import PIL
import io
from dotenv import load_dotenv
# from fastapi.security import OAuth2PasswordBearer
load_dotenv()

from app.routes.users import user_router
from app.routes.auth import router
from app.db import Base, engine, SessionLocal
from app.auth.auth_handler import get_current_user

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
        raise

app = FastAPI()
app.include_router(user_router, prefix="/users")
app.include_router(router, prefix="/auth")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://autodev-frontend.vercel.app"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.post("/upload")
async def sketch_to_code(file: UploadFile, req: Request, db: Session= Depends(get_db)):
    if not req.headers["authorization"].split(" ")[1]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = req.headers["authorization"].split(" ")[1]
    await get_current_user(token, db)
    try:
        os.mkdir("uploads")
        image_bytes = await file.read()
        image = PIL.Image.open(io.BytesIO(image_bytes))
        image.save("uploads/" + file.filename)
        response = model.generate_content(["Convert the image into HTML, CSS and JavaScript equivalent code only the frontend or UI not the backend. If the image can't be converted, return 'Failed to process image'. Use internal CSS and Javascript, add proper styling, include all the features, Make the code fully functional.", image])
        # print(response.text)
        os.remove(f"uploads/{file.filename}")
        os.rmdir("uploads")
        return response.text
    except:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while sending image to LLM for getting code response"
        )

# if __name__=="__main__":
#     uvicorn.run(app)