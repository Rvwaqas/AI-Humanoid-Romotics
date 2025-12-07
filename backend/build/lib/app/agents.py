from pydantic import BaseModel
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled,
    input_guardrail, GuardrailFunctionOutput, RunContextWrapper,
    output_guardrail, OutputGuardrailTripwireTriggered, InputGuardrailTripwireTriggered
)
from agents.run import RunConfig
from .config import settings
from .vector_store import search_book_content

# Setup Gemini provider and model
provider = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)
set_tracing_disabled(disabled=True)
config = RunConfig(model)

# RAG Tool for Agents
async def rag_search_tool(question: str, context: str = "") -> str:
    """RAG tool - searches book content"""
    if context.strip():
        # This part of the logic answers based on user-selected text
        return f"📖 Context: {context[:300]}"
    
    return await search_book_content(question)

# Guardrail Models
class CheckBookQuestion(BaseModel):
    is_book_question: bool
    reasoning: str

class CheckBookContext(BaseModel):
    is_book_related: bool
    reasoning: str

class Response(BaseModel):
    response: str

# Guardrail Agents
guardrail_agent = Agent(
    name="guardrail_agent",
    instructions="Check if user asks about book content, Physical AI, RAG, or robotics. Return true if relevant.",
    model=model,
    output_type=CheckBookQuestion
)

guardrail_out = Agent(
    name="guardrail_out",
    instructions="Ensure response is about book content only. Reject off-topic answers.",
    output_type=CheckBookContext,
    model=model
)

@input_guardrail
async def book_guardrail(ctx: RunContextWrapper, agent: Agent, input: str):
    result = await Runner.run(guardrail_agent, input)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_book_question
    )

@output_guardrail
async def output_guardrail_func(ctx: RunContextWrapper, agent: Agent, output: Response):
    result = await Runner.run(guardrail_out, output.response, context=ctx.context, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_book_related
    )

# Main RAG Agent with Qdrant Tool
rag_agent = Agent(
    name="rag_agent",
    instructions="Search book content using rag_search_tool. Answer based on retrieved context only.",
    tools=[rag_search_tool]
)

# Main Agent (Orchestrator)
main_agent = Agent(
    name="book_chatbot",
    instructions="You are a book assistant for Physical AI content. Use rag_agent for searches. Only answer book-related questions.",
    handoffs=[rag_agent],
    input_guardrails=[book_guardrail],
    output_guardrails=[output_guardrail_func],
    output_type=Response,
    model=model
)
