from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.deps import get_current_user
from app.models.models import User, Tenant
from app.schemas.schemas import OnboardResponse
from groq import Groq
from app.config import settings
from typing import List
from pydantic import BaseModel

router = APIRouter()
client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """You are onboarding a founder into their AI memory system.
Ask them about their business one question at a time — industry, product, team size, key people, current challenges.
After 5-6 exchanges say ONBOARDING_COMPLETE and summarize what you learned.
Do NOT repeat questions you have already asked."""

class Message(BaseModel):
    role: str
    content: str

class OnboardRequest(BaseModel):
    message: str
    history: List[Message] = []

@router.post("/chat", response_model=OnboardResponse)
def onboard_chat(data: OnboardRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in data.history:
        messages.append({"role": m.role, "content": m.content})
    messages.append({"role": "user", "content": data.message})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )
    reply = response.choices[0].message.content
    done = "ONBOARDING_COMPLETE" in reply

    if done:
        tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
        tenant.description = reply
        db.commit()

    return {"reply": reply, "done": done}