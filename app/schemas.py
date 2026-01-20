from pydantic import BaseModel

class ClaimRequest(BaseModel):
    claim: str

class ClaimResult(BaseModel):
    score: float
    claim: str
    verdict: str
    evidence: str
    date: str
