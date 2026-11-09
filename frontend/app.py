
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Claim Intelligence | AI Investigation",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2026 MODERN SAAS DESIGN
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1120;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: #101a2d;
    border-right: 1px solid #25334a;
}

[data-testid="stSidebar"] * {
    color: #dbeafe;
}

.main .block-container {
    padding: 2rem 3rem;
    max-width: 1500px;
}

.hero {
    background: linear-gradient(120deg, #142b49, #123c55, #164e63);
    border: 1px solid #28536d;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 25px;
}

.hero h1 {
    color: #ffffff;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #bfdbfe;
    font-size: 14px;
}

.section-title {
    color: #f1f5f9;
    font-size: 21px;
    font-weight: 700;
    margin: 25px 0 15px 0;
}

.metric-card {
    background: linear-gradient(145deg, #17243a, #111c30);
    border: 1px solid #293c57;
    border-radius: 16px;
    padding: 20px;
    min-height: 115px;
}

.metric-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: #67e8f9;
    font-size: 29px;
    font-weight: 800;
    margin-top: 10px;
}

.upload-card {
    background: #111c30;
    border: 1px solid #2b405c;
    border-radius: 18px;
    padding: 22px;
}

.info-card {
    background: #142238;
    border: 1px solid #2b405c;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
}

div.stButton > button {
    background: linear-gradient(90deg, #0891b2, #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 12px 22px;
    width: 100%;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    color: white;
    border: none;
}

.stTextInput input {
    background: #17243a;
    color: white;
    border: 1px solid #334155;
    border-radius: 9px;
}

[data-testid="stFileUploader"] {
    background: #142238;
    border: 1px dashed #3b82a0;
    border-radius: 14px;
    padding: 15px;
}

.stTextArea textarea {
    background: #101c30;
    color: #cbd5e1;
}

.footer {
    color: #64748b;
    font-size: 12px;
    text-align: center;
    padding: 25px 0;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🛡️ ClaimAI")
    st.caption("INTELLIGENCE PLATFORM")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Investigation", "About Project"],
        label_visibility="visible"
    )

    st.divider()
    st.markdown("### System Status")
    st.success("Dashboard Active")
    st.info(f"API: {API_URL}")

    st.markdown("---")
    st.caption("AI-powered insurance investigation")
    st.caption("Version 2.0 • 2026")

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>Insurance Claim Intelligence</h1>
    <p>
        AI-powered document intelligence, OCR extraction and
        explainable claim investigation signals.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------
if page == "About Project":
    st.markdown("## About ClaimAI")
    st.markdown("""
    This prototype demonstrates an AI-assisted insurance
    claim investigation workflow.

    **Core capabilities**
    - Document OCR and text extraction
    - AI-assisted factual summarization
    - Explainable review indicators
    - Evidence-based investigation workflow
    - Human-in-the-loop decision support
    """)
    st.stop()

# --------------------------------------------------
# DASHBOARD / INVESTIGATION
# --------------------------------------------------
st.markdown('<div class="section-title">📄 Claim Investigation Workspace</div>',
            unsafe_allow_html=True)

left, right = st.columns([1.35, 1])

with left:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)

    st.markdown("### Upload Claim Document")
    st.caption("Upload a scanned insurance claim or supporting document.")

    claim_id = st.text_input(
        "Claim Reference",
        value="CLM-DEMO-001"
    )

    uploaded = st.file_uploader(
        "Choose claim document",
        type=["pdf", "png", "jpg", "jpeg", "tif", "tiff"]
    )

    analyze = st.button(
        "🚀 Analyze Insurance Claim",
        type="primary",
        disabled=uploaded is None
    )

    if uploaded:
        st.success(f"Document ready: {uploaded.name}")
        st.caption(f"File size: {uploaded.size / 1024:.1f} KB")

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI Investigation Pipeline")
    st.markdown("""
    1. 📥 Document ingestion
    2. 🔍 OCR text extraction
    3. 🧩 Evidence analysis
    4. 🤖 AI factual summarization
    5. 🚩 Review signal detection
    6. 👨‍💼 Human decision
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# API REQUEST
# --------------------------------------------------
if analyze and uploaded:
    with st.spinner("Analyzing document and processing evidence..."):
        try:
            response = requests.post(
                f"{API_URL}/claims/analyze",
                data={"claim_id": claim_id},
                files={
                    "file": (
                        uploaded.name,
                        uploaded.getvalue(),
                        uploaded.type or "application/octet-stream"
                    )
                },
                timeout=180
            )

            if not response.ok:
                st.error(f"API Error ({response.status_code})")
                st.code(response.text)

            else:
                data = response.json()

                st.divider()
                st.markdown("## 📊 Investigation Results")

                # METRICS
                c1, c2, c3 = st.columns(3)

                with c1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">OCR Characters</div>
                        <div class="metric-value">{data.get('character_count', 0):,}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Review Priority</div>
                        <div class="metric-value">{data.get('review_priority', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                signals = data.get("fraud_signals", [])

                with c3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Review Signals</div>
                        <div class="metric-value">{len(signals)}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # AI SUMMARY
                summary = data.get("llm_summary")

                if summary:
                    st.markdown(
                        '<div class="section-title">🤖 AI Factual Summary</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.write(summary)
                    st.markdown('</div>', unsafe_allow_html=True)

                # REVIEW SIGNALS
                st.markdown(
                    '<div class="section-title">🚩 Investigation Review Signals</div>',
                    unsafe_allow_html=True
                )

                if signals:
                    for signal in signals:
                        severity = signal.get("severity", "unknown").upper()
                        code = signal.get("code", "REVIEW")
                        description = signal.get("description", "No description")
                        evidence = signal.get("evidence", "No evidence provided")

                        with st.expander(f"⚠️ {code} — {severity}", expanded=True):
                            st.write(description)
                            st.markdown("**Evidence identified:**")
                            st.info(evidence)
                else:
                    st.success(
                        "No configured review signals detected. "
                        "This does not establish that the claim is valid."
                    )

                # OCR TEXT
                st.markdown(
                    '<div class="section-title">🔍 Extracted Document Evidence</div>',
                    unsafe_allow_html=True
                )

                with st.expander("View complete OCR extraction"):
                    st.text(data.get("extracted_text", "No text extracted."))

                st.success("Investigation workflow completed.")

                st.caption(data.get("disclaimer", ""))

        except requests.RequestException as exc:
            st.error(f"Could not connect to backend: {exc}")
            st.info("Make sure FastAPI is running on the configured API URL.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown("""
<div class="footer">
    ClaimAI Intelligence Platform • 2026<br>
    Prototype only. AI-generated signals are not proof of fraud.
    Final claim decisions require qualified human review.
</div>
""", unsafe_allow_html=True)
