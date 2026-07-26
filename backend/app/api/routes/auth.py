from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Tenant
from app.schemas.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.core.auth import create_access_token
import bcrypt

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    tenant = Tenant(company_name=data.company_name)
    db.add(tenant)
    db.flush()

    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    user = User(
        tenant_id=tenant.id,
        name=data.name,
        email=data.email,
        hashed_password=hashed
    )
    db.add(user)
    db.commit()

    token = create_access_token({"sub": user.email, "tenant_id": str(tenant.id)})
    return {"access_token": token}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not bcrypt.checkpw(data.password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "tenant_id": str(user.tenant_id)})
    return {"access_token": token}