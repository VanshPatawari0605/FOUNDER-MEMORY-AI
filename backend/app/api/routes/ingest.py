from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.deps import get_current_user
from app.models.models import User, Document
from app.schemas.schemas import IngestResponse
from app.services.ingestion import process_file
import uuid

router = APIRouter()

ALLOWED_TYPES = ["application/pdf", "text/plain",
                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]

@router.post("/upload", response_model=IngestResponse)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    contents = await file.read()

    doc = Document(
        tenant_id=current_user.tenant_id,
        filename=file.filename,
        doc_type=file.content_type
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    process_file.delay(str(doc.id), str(current_user.tenant_id), file.filename, contents, file.content_type)

    return {"document_id": doc.id, "filename": file.filename, "status": "processing"}