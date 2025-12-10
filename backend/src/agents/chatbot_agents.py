import os
from agents import Agent, function_tool, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

embedder = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

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
