from pydantic import BaseModel, Field
from typing import List, Optional

class FraudSignal(BaseModel):
    code: str
    description: str
    severity: str = Field(pattern="^(low|medium|high)$")
    evidence: str

class ClaimAnalysis(BaseModel):
    claim_id: str
    filename: str
    extracted_text: str
    character_count: int
    fraud_signals: List[FraudSignal]
    review_priority: str
    llm_summary: Optional[str] = None
    disclaimer: str = (
        "Decision-support output only. This is not a fraud finding or claim denial. "
        "A qualified human reviewer must verify all evidence."
    )
