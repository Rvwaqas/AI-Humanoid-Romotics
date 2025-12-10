from fastapi import APIRouter
from agents import Runner
from src.models.schemas import QueryRequest, QueryResponse
from src.agents.chatbot_agents import main_agent, config

router = APIRouter()

@router.post("/chat", response_model=QueryResponse)
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
