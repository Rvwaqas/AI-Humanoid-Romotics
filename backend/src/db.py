import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

async def get_db():
    conn = await psycopg.AsyncConnection.connect(os.getenv("NEON_DATABASE_URL"))
    try:
        yield conn
    finally:
        await conn.close()
