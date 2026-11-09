from typing import TypedDict, Any
from langgraph.graph import StateGraph, END

class InvestigationState(TypedDict, total=False):
    claim_text: str
    signals: list
    priority: str
    summary: str | None

def evidence_review_node(state: InvestigationState) -> dict:
    from backend.services.fraud_rules import detect_review_signals, priority_from_signals
    signals = detect_review_signals(state["claim_text"])
    return {
        "signals": [s.model_dump() for s in signals],
        "priority": priority_from_signals(signals),
    }

def summary_node(state: InvestigationState) -> dict:
    from backend.services.llm import summarize_claim
    return {"summary": summarize_claim(state["claim_text"])}

def build_graph():
    workflow = StateGraph(InvestigationState)
    workflow.add_node("evidence_review", evidence_review_node)
    workflow.add_node("claim_summary", summary_node)
    workflow.set_entry_point("evidence_review")
    workflow.add_edge("evidence_review", "claim_summary")
    workflow.add_edge("claim_summary", END)
    return workflow.compile()

def run_investigation(text: str) -> dict[str, Any]:
    return build_graph().invoke({"claim_text": text})
