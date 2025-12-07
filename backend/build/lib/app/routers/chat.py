from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from ..agents import (
    main_agent, Runner, config,
    InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
)
from ..database import save_query
from ..vector_store import ingest_content as ingest_vector_content

router = APIRouter()

# Pydantic models for request/response
class ChatRequest(BaseModel):
    question: str
    context: str = ""

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

class IngestRequest(BaseModel):
    content: List[str]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handles the main chat logic using the agent architecture."""
    try:
        result = await Runner.run(
            main_agent,
            request.question,
            context={"user_context": request.context},
            run_config=config
        )
        answer = result.final_output.response
        
        # Save to Neon DB
        await save_query(request.question, answer, request.context)
        
        return ChatResponse(answer=answer, sources=[])
        
    except InputGuardrailTripwireTriggered:
        return ChatResponse(answer="❌ Please ask about book content only (Physical AI, RAG, robotics)", sources=[])
    except OutputGuardrailTripwireTriggered:
        return ChatResponse(answer="❌ Response must be book-related only", sources=[])
    except Exception as e:
        return ChatResponse(answer=f"Error: {str(e)}", sources=[])

@router.post("/ingest")
async def ingest(request: IngestRequest):
    """Handles content ingestion."""
    count = await ingest_vector_content(request.content)
    return {"status": "✅ Ingested", "count": count}
