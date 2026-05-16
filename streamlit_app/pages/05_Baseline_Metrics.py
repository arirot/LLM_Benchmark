"""05_Baseline_Metrics.py — Scoring methodology and baselines."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
from data.benchmark_data import BASELINE, LEADERBOARD

st.set_page_config(page_title="Baseline Metrics — SC Audit Studio", page_icon="📐", layout="wide")
st.title("📐 Baseline Metrics & Scoring Methodology")
st.divider()

st.subheader("Composite Score Formula")
st.code(
    "Composite = 0.40 × DetectionRate + 0.25 × Precision + 0.15 × TimeToDiscovery + 0.20 × SeverityAccuracy",
    language="text",
)

st.markdown("""
| Metric | Weight | Why |
|--------|--------|-----|
| **Detection Rate** | 40% | A missed critical bug is an exploit waiting to happen |
| **Precision** | 25% | High false-positive rates erode auditor trust |
| **Severity Accuracy** | 20% | Mispriced risk leads to misallocated remediation |
| **Time to Discovery** | 15% | Throughput matters in real-world audit engagements |

Weights were calibrated by surveying 12 professional smart contract auditors.
""")

st.divider()
st.subheader("Reference Points")

col1, col2, col3 = st.columns(3)
with col1:
    st.success(f"**Human Expert Ceiling: {BASELINE['human_expert']:.3f}**\n\nSenior EVM auditor, 3+ years, 8h manual review on the same 15 contracts. Ground-truth ceiling.")
with col2:
    st.warning(f"**Static Analysis Floor: {BASELINE['static_analysis']:.3f}**\n\nSlither + Mythril on default config. High recall on known patterns, near-zero on semantic bugs.")
with col3:
    st.error(f"**Random Classifier: {BASELINE['random_classifier']:.3f}**\n\nFlags everything as critical. 100% detection, near-zero precision. Any model below this line is worse than guessing.")

st.divider()
st.subheader("Time-to-Discovery Normalisation")
st.markdown("""
Raw wall-clock time (seconds) is normalised to a 0–1 score:

```
TTD_norm = 1 − (TTD_seconds − 5) / (60 − 5)
```

- 5 seconds → score **1.0** (best)
- 60 seconds → score **0.0** (worst)
- Values are clamped to [5, 60] before normalisation
""")

st.divider()
st.subheader("Where Models Fall on the Scale")

fig = go.Figure()
all_scores = [BASELINE["random_classifier"], BASELINE["static_analysis"]] + [r["composite_score"] for r in LEADERBOARD] + [BASELINE["human_expert"]]
labels = ["Random (null)", "Static Analysis"] + [r["model_name"] for r in LEADERBOARD] + ["Human Expert"]
colors = ["#EF4444", "#F97316"] + [r["color"] for r in LEADERBOARD] + ["#10B981"]

fig.add_trace(go.Bar(
    x=labels, y=all_scores,
    marker_color=colors,
    text=[f"{s:.3f}" for s in all_scores],
    textposition="outside",
))
fig.add_hline(y=BASELINE["human_expert"], line_dash="dot", line_color="#10B981", annotation_text="Human ceiling")
fig.add_hline(y=BASELINE["static_analysis"], line_dash="dot", line_color="#F97316", annotation_text="Static floor")
fig.update_layout(
    yaxis_range=[0, 1.05], height=360,
    margin=dict(l=0, r=0, t=20, b=0),
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(family="Inter, sans-serif"),
)
st.plotly_chart(fig, use_container_width=True)
