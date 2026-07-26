from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.deps import get_current_user
from app.models.models import User, Entity, Promise
from app.schemas.schemas import EntityOut, PromiseOut
from typing import List

router = APIRouter()

@router.get("/people", response_model=List[EntityOut])
def get_people(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Entity).filter(
        Entity.tenant_id == current_user.tenant_id,
        Entity.entity_type == "person"
    ).all()

@router.get("/promises", response_model=List[PromiseOut])
def get_promises(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Promise).filter(
        Promise.tenant_id == current_user.tenant_id
    ).all()

@router.get("/all", response_model=List[EntityOut])
def get_all_entities(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Entity).filter(
        Entity.tenant_id == current_user.tenant_id
    ).all()