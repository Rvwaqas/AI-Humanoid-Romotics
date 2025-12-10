from fastapi import APIRouter
from typing import List
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import os

router = APIRouter()

embedder = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

@router.post("/ingest")
async def ingest_content(texts: List[str]):
    vectors = embedder.encode(texts).tolist()
    points = [
        PointStruct(id=i, vector=vec, payload={"text": texts[i], "chapter": f"ch{i}"})
        for i, vec in enumerate(vectors)
    ]
    qdrant_client.upsert(collection_name="physical_ai_book", points=points)
    return {"status": "✅ Physical AI book ingested!", "chunks": len(texts)}
