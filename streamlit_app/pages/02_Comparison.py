"""02_Comparison.py — Side-by-side metric comparison matrix."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data.benchmark_data import LEADERBOARD, CATEGORY_BREAKDOWN

st.set_page_config(page_title="Comparison — SC Audit Studio", page_icon="📊", layout="wide")
st.title("📊 Comparison Matrix")
st.markdown("Side-by-side breakdown of every metric across all models.")
st.divider()

# Bar chart per metric
metrics = [
    ("Detection Rate", "detection_rate", "#EF4444"),
    ("Precision", "precision", "#F97316"),
    ("Severity Accuracy", "severity_accuracy", "#6366F1"),
    ("Time to Discovery (norm)", "time_to_discovery", "#06B6D4"),
]

cols = st.columns(2)
for i, (label, key, color) in enumerate(metrics):
    fig = go.Figure(go.Bar(
        x=[r["model_name"] for r in LEADERBOARD],
        y=[r[key] * 100 for r in LEADERBOARD],
        marker_color=[r["color"] for r in LEADERBOARD],
        text=[f"{r[key]*100:.1f}%" for r in LEADERBOARD],
        textposition="outside",
    ))
    fig.update_layout(
        title=label, yaxis_range=[0, 110],
        height=260, margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=12),
    )
    with cols[i % 2]:
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# Category heatmap
st.subheader("Detection by Vulnerability Category")
model_ids = ["gpt-4", "claude", "gemini", "copilot"]
model_labels = ["GPT-4", "Claude", "Gemini", "Copilot"]
categories = list(CATEGORY_BREAKDOWN.keys())
z = [[CATEGORY_BREAKDOWN[cat][mid] for mid in model_ids] for cat in categories]

fig2 = go.Figure(go.Heatmap(
    z=z, x=model_labels, y=categories,
    colorscale="Blues",
    text=[[f"{v}%" for v in row] for row in z],
    texttemplate="%{text}",
    showscale=True,
))
fig2.update_layout(height=360, margin=dict(l=0, r=0, t=20, b=0),
                   paper_bgcolor="white", font=dict(family="Inter, sans-serif"))
st.plotly_chart(fig2, use_container_width=True)
