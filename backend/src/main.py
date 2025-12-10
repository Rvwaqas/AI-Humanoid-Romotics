from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import auth, chat, ingest
import os
import psycopg
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

app = FastAPI(title="🏆 Physical AI Hackathon - Auth + RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(chat.router, tags=["Chatbot"])
app.include_router(ingest.router, tags=["Ingestion"])

@app.on_event("startup")
async def startup():
    """Create Neon tables + Qdrant collection"""
    async with await psycopg.AsyncConnection.connect(os.getenv("NEON_DATABASE_URL")) as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
    
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    qdrant_client.recreate_collection(
        collection_name="physical_ai_book",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print("✅ Hackathon backend ready! Neon + Qdrant + Agents + Auth")

@app.get("/")
async def root():
    return {
        "message": "🏆 Physical AI Hackathon Backend LIVE!",
        "endpoints": {
            "signup": "POST /signup {username, email, password}",
            "login": "POST /token {username, password}",
            "chat": "POST /chat {question}"
        }
    }
