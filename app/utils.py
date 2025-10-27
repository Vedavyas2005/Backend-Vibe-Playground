from fastapi import HTTPException

async def get_user_uid(id_token: str, verify_token_func):
    decoded = verify_token_func(id_token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return decoded.get("uid")
