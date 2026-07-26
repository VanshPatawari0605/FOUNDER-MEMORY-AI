from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, onboard, ingest, agent, entities
from app.database import engine
from app import models
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

models.models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Founder Memory AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(onboard.router, prefix="/onboard", tags=["onboard"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(agent.router, prefix="/agent", tags=["agent"])
app.include_router(entities.router, prefix="/entities", tags=["entities"])

@app.get("/")
def root():
    return {"status": "Founder Memory AI running"}