from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from backend.schemas import ClaimAnalysis, FraudSignal
from backend.services.ocr import extract_text
from backend.services.graph import run_investigation

app = FastAPI(
    title="Insurance Claim Investigation API",
    version="0.1.0",
    description="AI-assisted claim document extraction and human-review signals."
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/claims/analyze", response_model=ClaimAnalysis)
async def analyze_claim(
    file: UploadFile = File(...),
    claim_id: str = Form(default="UNASSIGNED")
):
    content = await file.read()
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds 15 MB limit.")
    try:
        text = extract_text(content, file.filename or "upload")
        result = run_investigation(text)
        return ClaimAnalysis(
            claim_id=claim_id,
            filename=file.filename or "upload",
            extracted_text=text,
            character_count=len(text),
            fraud_signals=[FraudSignal(**item) for item in result.get("signals", [])],
            review_priority=result.get("priority", "routine_human_review"),
            llm_summary=result.get("summary"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {type(exc).__name__}")
