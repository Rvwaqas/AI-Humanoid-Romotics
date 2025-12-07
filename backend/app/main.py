from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import chat
from .database import connect_to_db, close_db_connection
from .vector_store import setup_collection

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    print("--- Application Startup ---")
    await connect_to_db()
    setup_collection()
    print("--- Application Ready ---")
    yield
    print("--- Application Shutdown ---")
    await close_db_connection()
    print("--- Application Shutdown Complete ---")

app = FastAPI(
    title="RAG Book Chatbot - Refactored",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the chat router
app.include_router(chat.router)

@app.get("/health", tags=["Status"])
async def health():
    """Health check endpoint."""
    return {"status": "✅ Refactored RAG App is running"}

# The following is no longer needed as uvicorn will be run from the command line
# if __name__ == "__main__":
#     import uvicorn
#     from .app.config import settings
#     uvicorn.run(app, host="0.0.0.0", port=settings.PORT)