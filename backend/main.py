from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import psycopg

# 🔥 YOUR OpenAI Agents imports (FIXED)
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents import function_tool, RunConfig, set_tracing_disabled
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI(title="🏆 Physical AI Hackathon - Auth + RAG")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ✅ YOUR CONNECTIONS
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
embedder = SentenceTransformer('all-MiniLM-L6-v2')


# 🔥 YOUR Gemini Agents (UPDATED MODEL)
gemini_key = os.getenv("GEMINI_API_KEY")
provider = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",  # ✅ Fixed model name
    openai_client=provider
)
set_tracing_disabled(disabled=True)
config = RunConfig(model)


# 🔥 AUTH SETUP
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-hackathon-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Pydantic Models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # ✅ user se password bhi aayega



class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class QueryRequest(BaseModel):
    question: str
    context: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]


# Neon DB Helper
async def get_db():
    conn = await psycopg.AsyncConnection.connect(os.getenv("NEON_DATABASE_URL"))
    try:
        yield conn
    finally:
        await conn.close()


# Auth Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.fetchrow("SELECT * FROM users WHERE email = $1", email)
    if user is None:
        raise credentials_exception
    return user


# 🔥 YOUR RAG TOOL (UPDATED)
@function_tool
async def rag_search(question: str, context: Optional[str] = None) -> str:
    """Panaversity Physical AI book RAG search"""
    if context and len(context) > 10:
        return f"📖 Selected text context: {context[:500]}..."
    
    try:
        query_emb = embedder.encode(question).tolist()
        hits = qdrant_client.search(
            collection_name="physical_ai_book",
            query_vector=query_emb,
            limit=3
        )
        sources = [hit.payload.get('text', '')[:200] + "..." for hit in hits]
        return f"📚 Physical AI book chunks: {' | '.join(sources)}"
    except:
        return "No book content found. Run ingest.py first!"


# 🔥 YOUR AGENTS
rag_agent = Agent(
    name="physical_ai_rag_agent",
    instructions="Search Physical AI textbook (ROS2, Gazebo, Isaac Sim, VLA) using rag_search tool. Return relevant book chunks.",
    tools=[rag_search]
)


main_agent = Agent(
    name="physical_ai_chatbot",
    instructions="""Panaversity Hackathon Physical AI assistant. Answer ONLY about:
    - ROS 2 (nodes, topics, URDF, rclpy)
    - Gazebo simulation (physics, sensors, SDF)
    - NVIDIA Isaac Sim (VSLAM, Nav2)
    - Vision-Language-Action (VLA, Whisper)
    
    Use rag_agent for book content. Structure: 1) Explanation 2) Code 3) Hackathon tip.""",
    handoffs=[rag_agent],
    model=model
)


# 🔥 UPDATED ROUTES - FIXED SIGNUP
@app.post("/signup")
async def signup(user: UserCreate, db=Depends(get_db)):
    """Create user with username, email, password (psycopg)"""
    print(f"Received signup request for user: {user.username}, email: {user.email}")
    print(f"Password length: {len(user.password)}")
    try:
        async with db.cursor() as cur:
            # Email already exists?
            await cur.execute(
                
                "SELECT COUNT(*) FROM users WHERE email = %s",
                (user.email,),
            )
            row = await cur.fetchone()
            existing = row[0] if row else 0

            if existing > 0:
                raise HTTPException(status_code=400, detail="Email already registered!")

            # ✅ Password user se lo, max 72 bytes
            raw_password = user.password[:72]
            hashed_password = get_password_hash(raw_password)

            # Insert user
            await cur.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
                """,
                (user.username, user.email, hashed_password),
            )

        return {
            "message": "✅ User created!",
            "login": f"Email: {user.email}, use your chosen password to login.",
        }

    except Exception as e:
        print("❌ SIGNUP ERROR:", e)
        raise HTTPException(status_code=500, detail=f"Signup failed: {e}")


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "SELECT username, email, password FROM users WHERE email = %s",
            (form_data.username,)
        )
        row = await cur.fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="❌ Wrong email/password")

    username, email, hashed_password = row
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=401, detail="❌ Wrong email/password")

    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/chat", response_model=QueryResponse)
async def chat_query(req: QueryRequest):
    """🏆 MAIN HACKATHON ENDPOINT - Public"""
    try:
        result = await Runner.run(
            main_agent, 
            req.question, 
            context={"user_context": req.context or "", "user": "Guest"},
            run_config=config
        )
        return QueryResponse(answer=str(result.final_output), sources=[])
    except Exception as e:
        return QueryResponse(answer=f"🤖 Error: {str(e)}", sources=[])


# YOUR EXISTING ENDPOINTS
@app.post("/ingest")
async def ingest_content(texts: List[str]):
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
        "endpoints": {
            "signup": "POST /signup {username, email}",
            "login": "POST /token {email, password=username123}",
            "chat": "POST /chat {question} (Bearer token required)"
        }
    }


@app.on_event("startup")
async def startup():
    """Create Neon tables + Qdrant collection"""
    # Create users table
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
    
    # Create Qdrant collection
    qdrant_client.recreate_collection(
        collection_name="physical_ai_book",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print("✅ Hackathon backend ready! Neon + Qdrant + Agents + Auth")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)