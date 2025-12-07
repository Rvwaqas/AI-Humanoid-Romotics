from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
from .config import settings

embedder = TextEmbedding(model_name='BAAI/bge-small-en')

qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)

COLLECTION_NAME = "book_content"

def setup_collection():
    """Creates the Qdrant collection if it doesn't exist."""
    try:
        qdrant_client.get_collection(collection_name=COLLECTION_NAME)
    except Exception:
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
        )
        print(f"Collection '{COLLECTION_NAME}' created.")

async def search_book_content(question: str) -> str:
    """Performs a vector search on the book content."""
    query_emb = embedder.embed(question)
    hits = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb[0].tolist(),
        limit=3
    )
    sources = [hit.payload.get('text', '')[:200] for hit in hits]
    return f"📚 Found: {' | '.join(sources)}"

async def ingest_content(content: list[str]):
    """Ingests a list of content strings into Qdrant."""
    vectors = embedder.embed(content)
    points = [
        models.PointStruct(
            id=i,
            vector=vec.tolist(),
            payload={"text": content[i]}
        )
        for i, vec in enumerate(vectors)
    ]
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(content)
