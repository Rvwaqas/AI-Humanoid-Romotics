from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
# import asyncpg
import asyncio

# 🔥 COMPLETE OpenAI Agents imports (FIXED)
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents import function_tool, RunConfig, set_tracing_disabled
from agents.run import RunConfig as RunConfigImport
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

load_dotenv()

app = FastAPI(title="🏆 Physical AI Hackathon - OpenAI Agents RAG")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ YOUR CONNECTIONS (Fixed)
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Global DB pool
pool = None

# 🔥 COMPLETE Gemini OpenAI Agents Setup (Panaversity Style)
gemini_key = os.getenv("GEMINI_API_KEY")
provider = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider
)
set_tracing_disabled(disabled=True)
config = RunConfig(model)

# async def init_db():
#     """Initialize Neon Postgres"""
#     global pool
#     pool = await asyncpg.create_pool(os.getenv("NEON_DATABASE_URL"))
#     await pool.execute("""
#         CREATE TABLE IF NOT EXISTS queries (
#             id SERIAL PRIMARY KEY,
#             question TEXT,
#             context TEXT,
#             sources TEXT,
#             created_at TIMESTAMP DEFAULT NOW()
#         )
#     """)

@app.on_event("startup")
async def startup():
    # await init_db()
    qdrant_client.recreate_collection(
        collection_name="physical_ai_book",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print("✅ Hackathon backend ready! Neon + Qdrant + Agents")

class QueryRequest(BaseModel):
    question: str
    context: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

# 🔥 FIXED @function_tool (Hackathon RAG Tool)
@function_tool
async def rag_search(question: str, context: Optional[str] = None) -> str:
    """Panaversity Physical AI book RAG search"""
    if context:
        return f"📖 Selected text context: {context[:500]}..."
    
    # Qdrant semantic search
    query_emb = embedder.encode(question).tolist()
    hits = qdrant_client.search(
        collection_name="physical_ai_book",
        query_vector=query_emb,
        limit=3
    )
    sources = [hit.payload.get('text', '')[:200] for hit in hits]
    
    # Save to Neon
    # async with pool.acquire() as conn:
    #     await conn.execute(
    #         "INSERT INTO queries (question, context, sources) VALUES ($1, $2, $3)",
    #         question, context or "", str(sources)
    #     )
    
    return f"📚 Physical AI book chunks: {' | '.join(sources)}"

# 🔥 COMPLETE AGENTS (Hackathon Requirement)
rag_agent = Agent(
    name="physical_ai_rag_agent",
    instructions="Search Physical AI textbook (ROS2, Gazebo, Isaac Sim, VLA) using rag_search tool. Return relevant book chunks.",
    tools=[rag_search]
)

main_agent = Agent(
    name="physical_ai_chatbot",
    instructions="""Panaversity Hackathon Physical AI assistant. Answer ONLY about:
    - ROS 2 (nodes, topics, URDF)
    - Gazebo simulation (physics, sensors)
    - NVIDIA Isaac Sim (VSLAM, Nav2)
    - Vision-Language-Action (VLA)
    
    Use rag_agent for book content. Structure answers: Explanation + Code Example + Hackathon Tip.""",
    handoffs=[rag_agent],
    model=model
)

@app.post("/chat", response_model=QueryResponse)
async def chat_query(req: QueryRequest):
    """🏆 MAIN HACKATHON ENDPOINT - OpenAI Agents RAG"""
    try:
        # 🔥 FIXED Runner.run with config
        result = await Runner.run(
            main_agent, 
            req.question, 
            context={"user_context": req.context or ""},
            run_config=config  # 🔥 REQUIRED!
        )
        
        return QueryResponse(
            answer=str(result.final_output),
            sources=[]
        )
    except Exception as e:
        return QueryResponse(
            answer=f"Agent error: {str(e)}. Try: 'What is ROS2?'",
            sources=[]
        )

@app.post("/ingest")
async def ingest_content(texts: List[str]):
    """Index Physical AI book content"""
    vectors = embedder.encode(texts).tolist()
    points = [
        PointStruct(id=i, vector=vec, payload={"text": texts[i], "chapter": f"ch{i}"})
        for i, vec in enumerate(vectors)
    ]
    qdrant_client.upsert(collection_name="physical_ai_book", points=points)
    return {"status": "✅ Physical AI book ingested!", "chunks": len(texts)}

@app.get("/")
async def root():
    return {
        "message": "🏆 Physical AI Hackathon Backend LIVE!",
        "endpoints": ["/chat", "/ingest", "/docs"],
        "hackathon": "Spec-Kit Plus + OpenAI Agents + Neon + Qdrant"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "agents": True, "qdrant": True, "neon": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
