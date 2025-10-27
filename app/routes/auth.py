from fastapi import APIRouter, HTTPException
from firebase_admin import auth
from app.schemas import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", summary="Sign up user")
async def signup(user: UserCreate):
    try:
        user_record = auth.create_user(email=user.email, password=user.password)
        return {"uid": user_record.uid, "email": user.email, "message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Login handled client-side via Firebase SDK (no password auth here)
