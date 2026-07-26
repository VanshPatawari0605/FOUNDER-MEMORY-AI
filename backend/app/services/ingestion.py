from app.celery_app import celery_app
from app.config import settings
from app.database import SessionLocal
from app.models.models import Chunk, Document
from app.services.embedding import get_embedding
from app.services.entity_extractor import extract_entities
import pdfplumber
import docx
import pandas as pd
import io
import uuid

def parse_file(filename: str, contents: bytes, content_type: str) -> str:
    if content_type == "application/pdf":
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(io.BytesIO(contents))
        return "\n".join(p.text for p in doc.paragraphs)

    elif content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(io.BytesIO(contents))
        return df.to_string()

    elif content_type == "text/plain":
        return contents.decode("utf-8")

    return ""

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

@celery_app.task
def process_file(doc_id: str, tenant_id: str, filename: str, contents: bytes, content_type: str):
    db = SessionLocal()
    try:
        text = parse_file(filename, contents, content_type)
        if not text.strip():
            return

        chunks = chunk_text(text)

        for i, chunk_content in enumerate(chunks):
            embedding = get_embedding(chunk_content)
            chunk = Chunk(
                tenant_id=uuid.UUID(tenant_id),
                document_id=uuid.UUID(doc_id),
                content=chunk_content,
                embedding=embedding,
                chunk_index=i
            )
            db.add(chunk)

        db.commit()
        extract_entities.delay(doc_id, tenant_id, text)

    finally:
        db.close()