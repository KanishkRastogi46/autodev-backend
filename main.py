import uvicorn

from fastapi import FastAPI, UploadFile, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.post("/upload")
async def sketch_to_code(file: UploadFile):
    try:
        os.mkdir("uploads")
        image_bytes = await file.read()
        image = PIL.Image.open(io.BytesIO(image_bytes))
        image.save("uploads/" + file.filename)
        response = model.generate_content(["The image data that is provided to you will contain an image or rough sketch of a website, so you need to provide html, css and js code for that website and also keep in mind that css and js code should be inside that html tag only. Incase an image data can't be converted to html code then respond as follows:- 'Provide a proper image which contains information about website'", image])
        print(response.text)
        os.remove(f"uploads/{file.filename}")
        os.rmdir("uploads")
        return response.text
    except:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while sending image to LLM for getting code response"
        )

if __name__=="__main__":
    uvicorn.run(app)