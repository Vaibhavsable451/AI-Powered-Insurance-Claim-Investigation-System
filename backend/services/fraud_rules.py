import re
from typing import List
from backend.schemas import FraudSignal

# Transparent review prompts only; these rules do not establish fraud.
def detect_review_signals(text: str) -> List[FraudSignal]:
    normalized = text.lower()
    signals = []
    dates = re.findall(r"\\b(?:\\d{1,2}[/-]){2}\\d{2,4}\\b", text)

    if len(dates) >= 2 and len(set(dates)) == 1:
        signals.append(FraudSignal(
            code="REPEATED_DATE",
            description="The same date appears repeatedly; verify whether this is expected.",
            severity="low",
            evidence=f"Repeated date string: {dates[0]}"
        ))
    if any(x in normalized for x in ["handwritten correction", "overwritten", "altered amount"]):
        signals.append(FraudSignal(
            code="POSSIBLE_MANUAL_AMENDMENT",
            description="A manual amendment is mentioned; inspect the original document image.",
            severity="medium",
            evidence="Amendment-related wording detected by a keyword rule."
        ))
    if any(x in normalized for x in ["police report pending", "fir not available", "report unavailable"]):
        signals.append(FraudSignal(
            code="MISSING_SUPPORTING_REPORT",
            description="A supporting incident report may be unavailable or pending.",
            severity="medium",
            evidence="The document mentions a pending or unavailable report."
        ))
    if any(x in normalized for x in ["cash only", "no receipt", "receipt unavailable"]):
        signals.append(FraudSignal(
            code="RECEIPT_REVIEW",
            description="Payment evidence may need additional verification.",
            severity="low",
            evidence="The document mentions cash payment or an unavailable receipt."
        ))
    return signals

def priority_from_signals(signals: List[FraudSignal]) -> str:
    if any(s.severity == "high" for s in signals):
        return "urgent_human_review"
    if any(s.severity == "medium" for s in signals):
        return "standard_human_review"
    return "routine_human_review"
