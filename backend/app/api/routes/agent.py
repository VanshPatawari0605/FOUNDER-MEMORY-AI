from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.deps import get_current_user
from app.models.models import User, Tenant
from app.schemas.schemas import QueryRequest, QueryResponse
from app.agent.graph import run_agent

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query(data: QueryRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    company_context = tenant.description or "" if tenant else ""
    
    result = run_agent(
        question=data.question,
        tenant_id=str(current_user.tenant_id),
        db=db,
        company_context=company_context
    )
    return {"answer": result["answer"], "sources": result.get("sources", [])}