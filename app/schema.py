from pydantic import BaseModel

class Users(BaseModel):
    fullname: str | None = None
    email: str | None = None
    password: str | None = None