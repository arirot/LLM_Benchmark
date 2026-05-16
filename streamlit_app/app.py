"""
app.py — SC Audit Studio: LLM Benchmark
Main Streamlit entry point.

Run locally:
    streamlit run streamlit_app/app.py

Deploy to Streamlit Cloud:
    See docs/deployment.md
"""
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OPENAI_API_KEY, GOOGLE_API_KEY
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)


import streamlit as st

st.set_page_config(
    page_title="SC Audit Studio — LLM Benchmark",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — light theme matching the React dashboard
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Light theme overrides */
    [data-testid="stAppViewContainer"] { background: #F8FAFC; }
    [data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E2E8F0; }
    [data-testid="stSidebar"] .stMarkdown h2 { font-size: 1.1rem; color: #1E293B; }

    /* Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
    }
    .rank-badge {
        display: inline-block;
        font-family: monospace;
        font-size: 0.75rem;
        font-weight: 700;
        background: #EDE9FE;
        color: #6D28D9;
        padding: 2px 8px;
        border-radius: 4px;
    }
    /* Hide default Streamlit branding on the main page */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from data.benchmark_data import LEADERBOARD, MODELS, CATEGORY_BREAKDOWN, BASELINE

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛡️ SC Audit Studio")
    st.markdown("*LLM Benchmark — Smart Contract Security*")
    st.divider()
    st.markdown("""
**Navigate using the pages in the left sidebar.**

| Page | Description |
|------|-------------|
| 🏆 Leaderboard | Overall model rankings |
| 📊 Comparison | Side-by-side metrics |
| 🔍 Vulnerabilities | Test case dataset |
| 🤖 Model Registry | Model specs |
| 📐 Baseline Metrics | Scoring methodology |
| 📁 Custom Audit | Upload your .sol file |
    """)
    st.divider()
    st.caption("Benchmark date: May 2025 · 15 test cases · 4 models")

# ---------------------------------------------------------------------------
# Home — Leaderboard summary
# ---------------------------------------------------------------------------
st.title("🏆 Leaderboard")
st.markdown("Rankings of LLM performance on smart contract vulnerability detection.")
st.divider()

# Top model cards
cols = st.columns(4)
for col, entry in zip(cols, LEADERBOARD):
    with col:
        st.markdown(f"""
<div class="metric-card">
  <div><span class="rank-badge">Rank #{entry['rank']}</span></div>
  <div style="font-size:1.3rem;font-weight:700;margin-top:8px;font-family:monospace">
    {entry['model_name']}
  </div>
  <div style="color:#64748B;font-size:0.85rem;margin-top:4px">Composite Score</div>
  <div style="font-size:2rem;font-weight:800;color:{entry['color']}">
    {entry['composite_score']:.3f}
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Detailed rankings table
st.subheader("Detailed Rankings")
df = pd.DataFrame([
    {
        "Rank": f"#{r['rank']}",
        "Model": r["model_name"],
        "Composite Score": f"{r['composite_score']:.3f}",
        "Detection Rate": f"{r['detection_rate']*100:.1f}%",
        "Precision": f"{r['precision']*100:.1f}%",
        "Severity Accuracy": f"{r['severity_accuracy']*100:.1f}%",
        "Time to Discovery": f"{r['time_to_discovery']*100:.1f}",
    }
    for r in LEADERBOARD
])
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# Category heatmap
st.subheader("Detection Rate by Vulnerability Category")
categories = list(CATEGORY_BREAKDOWN.keys())
model_ids  = ["gpt-4", "claude", "gemini", "copilot"]
model_labels = ["GPT-4", "Claude", "Gemini", "Copilot"]
z_values = [[CATEGORY_BREAKDOWN[cat][mid] for mid in model_ids] for cat in categories]

fig = go.Figure(go.Heatmap(
    z=z_values,
    x=model_labels,
    y=categories,
    colorscale="Blues",
    text=[[f"{v}%" for v in row] for row in z_values],
    texttemplate="%{text}",
    showscale=True,
    colorbar=dict(title="Detection %"),
))
fig.update_layout(
    height=380,
    margin=dict(l=0, r=0, t=20, b=0),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Inter, sans-serif"),
)
st.plotly_chart(fig, use_container_width=True)
