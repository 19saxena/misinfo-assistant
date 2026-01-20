from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION = "misinformation_claims"

def search_claim(query: str, limit: int = 3):
    vector = model.encode(query).tolist()

    hits = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        limit=limit
    ).points

    return [
    {
        "id": hit.id,
        "score": hit.score,
        "claim": hit.payload["claim"],
        "verdict": hit.payload["verdict"],
        "evidence": hit.payload["evidence"],
        "image_url": hit.payload.get("image_url"),
        "times_seen": hit.payload.get("times_seen", 1),
        "date": hit.payload["date"]
    }
    for hit in hits
]


