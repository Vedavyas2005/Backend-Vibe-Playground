from pydantic import BaseModel, EmailStr
from typing import List

class User(BaseModel):
    uid: str
    email: EmailStr

class SessionCreate(BaseModel):
    session_id: str

class CodeSave(BaseModel):
    session_id: str
    code: str

class CodeRequest(BaseModel):
    prompt: str
