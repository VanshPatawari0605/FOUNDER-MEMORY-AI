from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

# Auth
class RegisterRequest(BaseModel):
    company_name: str
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Onboarding
class OnboardRequest(BaseModel):
    message: str

class OnboardResponse(BaseModel):
    reply: str
    done: bool = False

# Ingest
class IngestResponse(BaseModel):
    document_id: UUID
    filename: str
    status: str

# Agent
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = []

# Entities
class EntityOut(BaseModel):
    id: UUID
    name: str
    entity_type: str
    description: Optional[str]

    class Config:
        from_attributes = True

class PromiseOut(BaseModel):
    id: UUID
    person: str
    commitment: str
    date_mentioned: Optional[datetime]

    class Config:
        from_attributes = True