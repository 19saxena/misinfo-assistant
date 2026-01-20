import json
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer

COLLECTION = "misinformation_claims"

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create collection only if not exists
if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        ),
    )

with open("data/seed_claims.json", "r", encoding="utf-8") as f:
    claims = json.load(f)

vectors = model.encode([c["claim"] for c in claims]).tolist()

client.upsert(
    collection_name=COLLECTION,
    points=[
        {
            "id": idx,
            "vector": vectors[idx],
            "payload": claims[idx]
        }
        for idx in range(len(claims))
    ]
)

print("Seed data ingested into Qdrant")
