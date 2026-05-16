"""
06_Custom_Audit.py
Upload a .sol file and run it against selected LLM models.
"""

import time
import streamlit as st

st.set_page_config(page_title="Smart Contract Audit — SC Audit Studio", page_icon="📁", layout="wide")
st.title("📁 Smart Contract Audit")
st.markdown(
    "Upload your own Solidity smart contract and test it against any combination of LLM models. "
    "Accepted file type: `.sol` — max 500 KB."
)
st.divider()

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.llm_clients import MODEL_AUDIT_FN, get_available_models
from utils.parser import parse_findings, count_severity
from utils.scoring import normalise_ttd, composite_score

import pandas as pd
import plotly.graph_objects as go

SEVERITY_COLORS = {
    "critical": "#EF4444",
    "high":     "#F97316",
    "medium":   "#EAB308",
    "low":      "#64748B",
}

# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Contract File (.sol only)",
    type=["sol"],
    help="Upload a Solidity source file. Max 500 KB. Other file types are rejected.",
)

if uploaded_file:
    if uploaded_file.size > 500 * 1024:
        st.error("File too large. Maximum size is 500 KB.")
        st.stop()

    contract_code = uploaded_file.read().decode("utf-8", errors="replace")
    lines = contract_code.split("\n")
    st.success(f"Loaded **{uploaded_file.name}** — {len(lines)} lines, {uploaded_file.size / 1024:.1f} KB")

    with st.expander("Preview contract source"):
        st.code(contract_code, language="solidity", line_numbers=True)

    st.divider()

    # ---------------------------------------------------------------------------
    # Model selection
    # ---------------------------------------------------------------------------
    st.subheader("Select Models")

    available = get_available_models()
    model_options = {
        "gpt-4":   "GPT-4 Turbo (OpenAI)",
        "claude":  "Claude 3.5 Sonnet (Anthropic)",
        "gemini":  "Gemini 1.5 Pro (Google)",
        "copilot": "GitHub Copilot (GitHub/OpenAI)",
    }

    selected_models: list[str] = []
    col1, col2 = st.columns(2)
    for i, (mid, label) in enumerate(model_options.items()):
        col = col1 if i % 2 == 0 else col2
        with col:
            has_key = mid in available
            checked = col.checkbox(
                label,
                value=has_key,
                key=f"model_{mid}",
                help="API key not configured — add it to .env or Streamlit secrets." if not has_key else None,
                disabled=not has_key,
            )
            if checked and has_key:
                selected_models.append(mid)

    if not available:
        st.warning(
            "No API keys are configured. "
            "Add `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or `GITHUB_TOKEN` "
            "to your `.env` file (local) or Streamlit Secrets (cloud)."
        )

    st.divider()

    # ---------------------------------------------------------------------------
    # Run audit
    # ---------------------------------------------------------------------------
    run_clicked = st.button(
        "🔍 Run Audit",
        disabled=len(selected_models) == 0,
        type="primary",
    )

    if run_clicked:
        all_results = []
        progress = st.progress(0, text="Starting audit…")
        status_area = st.empty()

        for idx, model_id in enumerate(selected_models):
            status_area.info(f"Auditing with **{model_options[model_id]}**…")
            try:
                result = MODEL_AUDIT_FN[model_id](contract_code)
                findings = parse_findings(result["raw_response"])
                result["findings"] = findings
                result["severity_counts"] = count_severity(findings)
                all_results.append(result)
            except Exception as exc:
                st.error(f"**{model_options[model_id]}** failed: {exc}")
            progress.progress((idx + 1) / len(selected_models))

        progress.empty()
        status_area.empty()

        if not all_results:
            st.error("All model calls failed. Check your API keys.")
            st.stop()

        st.success(f"Audit complete — {len(all_results)} model(s) responded.")
        st.divider()

        # ---------------------------------------------------------------------------
        # Results
        # ---------------------------------------------------------------------------
        st.subheader("Results")

        # Score cards
        score_cols = st.columns(len(all_results))
        for col, r in zip(score_cols, all_results):
            total_findings = len(r["findings"])
            ttd_norm = normalise_ttd(r["time_seconds"])
            # Simplified scoring (without ground-truth matching)
            crit = r["severity_counts"]["critical"]
            high = r["severity_counts"]["high"]

            with col:
                st.markdown(f"""
<div style="background:#fff;border:1px solid #E2E8F0;border-top:4px solid {r['color']};
     border-radius:10px;padding:1rem;">
  <div style="font-family:monospace;font-weight:700;color:{r['color']}">{r['model_name']}</div>
  <div style="font-size:0.8rem;color:#64748B;margin-top:4px">{r['time_seconds']}s response time</div>
  <div style="font-size:2rem;font-weight:800;color:{r['color']};margin-top:8px">{total_findings}</div>
  <div style="font-size:0.8rem;color:#64748B">findings detected</div>
  <hr style="margin:8px 0;border-color:#F1F5F9"/>
  <div style="font-size:0.85rem">
    🔴 Critical: <b>{crit}</b> &nbsp; 🟠 High: <b>{high}</b>
  </div>
</div>
""", unsafe_allow_html=True)

        st.divider()

        # Per-model findings
        for r in all_results:
            with st.expander(f"**{r['model_name']}** — {len(r['findings'])} finding(s)", expanded=True):
                if not r["findings"]:
                    st.info("No vulnerabilities detected.")
                else:
                    for f in r["findings"]:
                        color = SEVERITY_COLORS.get(f.severity, "#64748B")
                        st.markdown(f"""
<div style="border:1px solid {color}33;border-left:4px solid {color};
     background:{color}08;border-radius:6px;padding:0.75rem 1rem;margin-bottom:0.6rem">
  <div style="display:flex;align-items:center;gap:8px">
    <span style="background:{color}20;color:{color};font-size:0.75rem;font-weight:700;
          font-family:monospace;padding:2px 8px;border-radius:4px">{f.severity.upper()}</span>
    <span style="font-weight:600">{f.title}</span>
    {"<span style='margin-left:auto;font-family:monospace;font-size:0.8rem;color:#64748B'>Line " + str(f.line) + "</span>" if f.line else ""}
  </div>
  <div style="margin-top:6px;font-size:0.9rem;color:#334155">{f.description}</div>
  <div style="margin-top:4px;font-size:0.85rem;color:#64748B">
    <b>Fix:</b> {f.recommendation}
  </div>
</div>
""", unsafe_allow_html=True)

                st.caption(f"Raw response time: {r['time_seconds']}s")

        st.divider()

        # Raw responses
        for r in all_results:
            with st.expander(f"Raw response — {r['model_name']}"):
                st.code(r["raw_response"], language="text")
