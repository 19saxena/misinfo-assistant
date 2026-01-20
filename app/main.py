from fastapi import FastAPI
from app.search import search_claim
from app.schemas import ClaimRequest
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Misinformation Memory Assistant")

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")
COLLECTION = "misinformation_claims"

@app.post("/check-claim")
def check_claim(req: ClaimRequest):
    results = search_claim(req.claim)

    # Filter out weak semantic matches
    SIMILARITY_THRESHOLD = 0.6
    filtered_results = [
        r for r in results if r["score"] >= SIMILARITY_THRESHOLD
    ]

    # CASE 1: Meaningful prior evidence exists → reinforce memory
    if filtered_results:
        top = filtered_results[0]
        point_id = top["id"]
        current_count = top.get("times_seen", 1)

        client.set_payload(
            collection_name=COLLECTION,
            payload={
                "times_seen": current_count + 1
            },
            points=[point_id]
        )

        return {
            "query": req.claim,
            "matches": filtered_results,
            "limitations": "This system retrieves past evidence and does not independently verify factual correctness."
        }

    # CASE 2: No relevant evidence → store as new memory
    else:
        vector = model.encode(req.claim).tolist()
        client.upsert(
            collection_name=COLLECTION,
            points=[
                {
                    "id": abs(hash(req.claim)) % (10**12),
                    "vector": vector,
                    "payload": {
                        "claim": req.claim,
                        "source": "User Input",
                        "date": "2026",
                        "verdict": "Unknown",
                        "evidence": "No prior evidence found.",
                        "image_url": None,
                        "times_seen": 1
                    }
                }
            ]
        )

        return {
            "query": req.claim,
            "matches": [],
            "message": "No relevant prior evidence found in memory.",
            "limitations": "This system retrieves past evidence and does not independently verify factual correctness."
        }
