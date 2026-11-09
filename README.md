
# Autonomous Insurance Claim Investigation — Starter

Learning prototype for insurance-document OCR and AI-assisted human review.

## Features
- PDF/image upload through Streamlit
- Tesseract OCR with PyMuPDF PDF rendering
- Pydantic response validation
- Explainable review indicators (not fraud verdicts)
- Optional Groq factual summary
- LangGraph investigation workflow
- FastAPI endpoint
- Optional FAISS evidence index module

## Setup
1. Install Tesseract OCR and ensure `tesseract` is on PATH.
   - Ubuntu: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`
   - Windows: install Tesseract OCR and set `TESSERACT_CMD` in `.env` if needed.
2. Create environment and install packages:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env`; optionally add your Groq API key.
4. Start API: `uvicorn backend.main:app --reload`
5. Start UI in another terminal: `streamlit run frontend/app.py`
6. API docs: http://127.0.0.1:8000/docs

## API
`POST /claims/analyze` multipart fields:
- `file`: PDF, PNG, JPG, JPEG, TIFF
- `claim_id`: optional string

Example:
```bash
curl -X POST http://127.0.0.1:8000/claims/analyze -F "claim_id=CLM-1001" -F "file=@claim.pdf"
```

## Important
This is a prototype, not a validated fraud-detection system. OCR and keyword indicators can be wrong. Never automatically deny or approve a claim based on this output. A qualified human must verify the original evidence. Add authentication, authorization, encryption, audit logging, privacy/retention controls, dataset validation, bias testing, and regulatory review before real deployment.

OCR is English-only by default. Handwriting and poor scans require a stronger document AI model and benchmarking.
=======
# AI-Powered-Insurance-Claim-Investigation-System

