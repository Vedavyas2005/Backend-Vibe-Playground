from fastapi import APIRouter, Header, HTTPException
from app.firebase import db, verify_token
from app.models import SessionCreate
from app.utils import get_user_uid

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", summary="Create new session")
async def create_session(session: SessionCreate, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    uid = await get_user_uid(token, verify_token)
    session_ref = db.collection("sessions").document(session.session_id)
    session_ref.set({"user_id": uid, "prompts": [], "codes": []})
    return {"session_id": session.session_id, "status": "created"}

@router.get("/{session_id}", summary="Get session data")
async def get_session(session_id: str, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    uid = await get_user_uid(token, verify_token)
    session_ref = db.collection("sessions").document(session_id)
    doc = session_ref.get()
    if not doc.exists or doc.to_dict().get("user_id") != uid:
        raise HTTPException(status_code=404, detail="Session not found or access denied")
    return doc.to_dict()
