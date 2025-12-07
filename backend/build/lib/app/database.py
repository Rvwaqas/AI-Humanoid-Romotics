import asyncpg
from .config import settings

pool: asyncpg.Pool = None

async def connect_to_db():
    """Connects to the database and initializes the connection pool."""
    global pool
    pool = await asyncpg.create_pool(settings.NEON_DATABASE_URL)
    await pool.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id SERIAL PRIMARY KEY,
            question TEXT,
            answer TEXT,
            context TEXT
        )
    """)
    print("Database connection pool created and table checked.")

async def close_db_connection():
    """Closes the database connection pool."""
    global pool
    if pool:
        await pool.close()
        print("Database connection pool closed.")

async def get_db_pool() -> asyncpg.Pool:
    """Returns the database connection pool."""
    return pool

async def save_query(question: str, answer: str, context: str):
    """Saves a query and its response to the database."""
    if not pool:
        raise RuntimeError("Database connection pool is not initialized.")
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO queries (question, answer, context) VALUES ($1, $2, $3)",
            question, answer, context
        )
