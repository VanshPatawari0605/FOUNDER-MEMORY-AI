from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.models import Entity, Promise
from groq import Groq
from app.config import settings
import uuid
import json

client = Groq(api_key=settings.GROQ_API_KEY)

EXTRACT_PROMPT = """Extract entities from this text. Return ONLY valid JSON, nothing else.

Format:
{{
  "people": [
    {{"name": "...", "description": "..."}}
  ],
  "promises": [
    {{"person": "...", "commitment": "...", "date_mentioned": null}}
  ],
  "companies": [
    {{"name": "...", "description": "..."}}
  ]
}}

Text:
{text}"""

@celery_app.task
def extract_entities(doc_id: str, tenant_id: str, text: str):
    db = SessionLocal()
    try:
        truncated = text[:3000]
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": EXTRACT_PROMPT.format(text=truncated)}
            ]
        )

        raw = response.choices[0].message.content
        clean = raw.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)

        for person in data.get("people", []):
            db.add(Entity(
                tenant_id=uuid.UUID(tenant_id),
                name=person["name"],
                entity_type="person",
                description=person.get("description"),
                source_doc_id=uuid.UUID(doc_id)
            ))

        for company in data.get("companies", []):
            db.add(Entity(
                tenant_id=uuid.UUID(tenant_id),
                name=company["name"],
                entity_type="company",
                description=company.get("description"),
                source_doc_id=uuid.UUID(doc_id)
            ))

        for promise in data.get("promises", []):
            db.add(Promise(
                tenant_id=uuid.UUID(tenant_id),
                person=promise["person"],
                commitment=promise["commitment"],
                source_doc_id=uuid.UUID(doc_id)
            ))

        db.commit()

    except Exception as e:
        print(f"Entity extraction failed: {e}")
    finally:
        db.close()