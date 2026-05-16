"""01_Leaderboard.py — Full leaderboard with radar chart."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data.benchmark_data import LEADERBOARD, BASELINE

st.set_page_config(page_title="Leaderboard — SC Audit Studio", page_icon="🏆", layout="wide")
st.title("🏆 Leaderboard")
st.markdown("Composite score ranking across all evaluated models.")
st.divider()

# Radar chart
metrics = ["Detection Rate", "Precision", "Severity Accuracy", "Time to Discovery"]
fig = go.Figure()
for entry in LEADERBOARD:
    values = [
        entry["detection_rate"] * 100,
        entry["precision"] * 100,
        entry["severity_accuracy"] * 100,
        entry["time_to_discovery"] * 100,
    ]
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=metrics + [metrics[0]],
        fill="toself",
        name=entry["model_name"],
        line=dict(color=entry["color"], width=2),
        fillcolor=entry["color"] + "22",
    ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    height=420,
    paper_bgcolor="white",
    font=dict(family="Inter, sans-serif"),
)
st.plotly_chart(fig, use_container_width=True)
st.divider()

# Reference lines
col1, col2, col3 = st.columns(3)
col1.metric("Human Expert Ceiling", f"{BASELINE['human_expert']:.3f}", help="Senior EVM auditor, 8h review")
col2.metric("Static Analysis Floor", f"{BASELINE['static_analysis']:.3f}", help="Slither + Mythril defaults")
col3.metric("Random Classifier Null", f"{BASELINE['random_classifier']:.3f}", help="Flags everything as critical")

st.divider()

# Full table
df = pd.DataFrame([
    {
        "Rank": f"#{r['rank']}",
        "Model": r["model_name"],
        "Composite": r["composite_score"],
        "Detection %": f"{r['detection_rate']*100:.1f}%",
        "Precision %": f"{r['precision']*100:.1f}%",
        "Sev. Accuracy %": f"{r['severity_accuracy']*100:.1f}%",
        "TTD (norm)": f"{r['time_to_discovery']*100:.1f}",
    }
    for r in LEADERBOARD
])
st.dataframe(df, use_container_width=True, hide_index=True)
