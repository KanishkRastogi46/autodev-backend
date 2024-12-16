from pydantic import BaseModel

class SendUser(BaseModel):
    email: str
    profile: str | None = None

class UserRegister(BaseModel):
    fullname: str | None = None
    email: str | None = None
    password: str | None = None
    confirmPassword: str | None = None
    
class RegisterResponse(BaseModel):
    message: str
    success: bool
    
class ChatResponse(BaseModel):
    Language: str
    Code: str
    Explanation: str
    Note: str
    success: bool
    
class ChatError(BaseModel):
    message: str
    success: bool
    
class Prompt(BaseModel):
    prompt: str
    
class LoginResponse(BaseModel):
    message: str
    user: SendUser
    access_token: str
    token_type: str
    success: bool
    
class LoginForm(BaseModel):
    email: str
    password: str
    
class VerifyEmail(BaseModel):
    email: str
    code: str