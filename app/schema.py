from pydantic import BaseModel

class Users(BaseModel):
    fullname: str | None = None
    email: str | None = None
    password: str | None = None
    
class ChatResponse(BaseModel):
    Language: str
    Code: str
    Explanation: str
    Note: str
    
class Prompt(BaseModel):
    prompt: str