from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class TokenRequest(BaseModel):
    id_token: str

class PromptRequest(BaseModel):
    prompt: str
    session_id: str
