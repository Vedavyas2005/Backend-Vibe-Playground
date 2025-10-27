from fastapi import APIRouter, HTTPException, Header
from app.firebase import db, verify_token
from app.models import CodeSave
from app.utils import get_user_uid
from app.gemini import generate_code
from app.schemas import PromptRequest

router = APIRouter(prefix="/code", tags=["code"])

@router.post("/save", summary="Save generated code to session")
async def save_code(code_data: CodeSave, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    uid = await get_user_uid(token, verify_token)
    session_ref = db.collection("sessions").document(code_data.session_id)
    doc = session_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Session not found")
    if doc.to_dict().get("user_id") != uid:
        raise HTTPException(status_code=403, detail="Permission denied")
    codes = doc.to_dict().get("codes", [])
    codes.append(code_data.code)
    session_ref.update({"codes": codes})
    return {"status": "code saved"}

@router.post("/generate", summary="Generate code using Gemini API")
async def generate_code_endpoint(request: PromptRequest, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    uid = await get_user_uid(token, verify_token)
    session_ref = db.collection("sessions").document(request.session_id)
    doc = session_ref.get()
    if not doc.exists or doc.to_dict().get("user_id") != uid:
        raise HTTPException(status_code=404, detail="Session not found or access denied")

    prompt_list = doc.to_dict().get("prompts", [])
    prompt_list.append(request.prompt)
    session_ref.update({"prompts": prompt_list})

    # Call Gemini LLM
    generated_code = await generate_code(request.prompt)

    codes_list = doc.to_dict().get("codes", [])
    codes_list.append(generated_code)
    session_ref.update({"codes": codes_list})

    return {"generated_code": generated_code}
