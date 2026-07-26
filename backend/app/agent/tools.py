from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.models import Chunk, Entity, Promise, Document
from app.services.embedding import get_embedding
import uuid

def search_memories(query: str, tenant_id: str, db: Session, k: int = 5) -> list[dict]:
    embedding = get_embedding(query)
    results = db.execute(
        text("""
            SELECT c.content, d.filename, c.chunk_index,
                   1 - (c.embedding <=> :embedding::vector) AS similarity
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE c.tenant_id = :tenant_id
            ORDER BY c.embedding <=> :embedding::vector
            LIMIT :k
        """),
        {"embedding": str(embedding), "tenant_id": tenant_id, "k": k}
    ).fetchall()

    return [
        {"content": r.content, "source": r.filename, "similarity": r.similarity}
        for r in results
    ]
def get_company_context(tenant_id: str, db: Session) -> str:
    from app.models.models import Tenant
    import uuid
    tenant = db.query(Tenant).filter(Tenant.id == uuid.UUID(tenant_id)).first()
    return tenant.description or "" if tenant else ""

def get_entity(name: str, tenant_id: str, db: Session) -> list[dict]:
    results = db.query(Entity).filter(
        Entity.tenant_id == uuid.UUID(tenant_id),
        Entity.name.ilike(f"%{name}%")
    ).all()

    return [
        {"name": e.name, "type": e.entity_type, "description": e.description}
        for e in results
    ]

def get_promises(person: str, tenant_id: str, db: Session) -> list[dict]:
    results = db.query(Promise).filter(
        Promise.tenant_id == uuid.UUID(tenant_id),
        Promise.person.ilike(f"%{person}%")
    ).all()

    return [
        {"person": p.person, "commitment": p.commitment, "date": str(p.date_mentioned)}
        for p in results
    ]

def get_timeline(topic: str, tenant_id: str, db: Session) -> list[dict]:
    results = db.execute(
        text("""
            SELECT c.content, d.filename, d.uploaded_at,
                   1 - (c.embedding <=> :embedding::vector) AS similarity
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE c.tenant_id = :tenant_id
            ORDER BY c.embedding <=> :embedding::vector, d.uploaded_at ASC
            LIMIT 10
        """),
        {"embedding": str(get_embedding(topic)), "tenant_id": tenant_id}
    ).fetchall()

    return [
        {"content": r.content, "source": r.filename, "date": str(r.uploaded_at)}
        for r in results
    ]
def get_company_context(tenant_id: str, db: Session) -> str:
    from app.models.models import Tenant
    import uuid
    tenant = db.query(Tenant).filter(Tenant.id == uuid.UUID(tenant_id)).first()
    return tenant.description or "" if tenant else ""