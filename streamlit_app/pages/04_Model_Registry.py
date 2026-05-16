"""04_Model_Registry.py — Model specs and configuration."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from data.benchmark_data import MODELS, LEADERBOARD

st.set_page_config(page_title="Model Registry — SC Audit Studio", page_icon="🤖", layout="wide")
st.title("🤖 Model Registry")
st.markdown("Specifications and benchmark results for each evaluated LLM.")
st.divider()

leaderboard_by_id = {r["model_id"]: r for r in LEADERBOARD}

for model in MODELS:
    lb = leaderboard_by_id.get(model["id"], {})
    with st.expander(f"**{model['full_name']}** — {model['provider']}", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Composite Score", f"{lb.get('composite_score', '—'):.3f}" if lb else "—")
        c2.metric("Context Window", f"{model['context_window']:,} tokens")
        c3.metric("Detection Rate", f"{lb.get('detection_rate', 0)*100:.1f}%" if lb else "—")
        c4.metric("Rank", f"#{lb.get('rank', '—')}" if lb else "—")

        st.markdown(f"**Version:** `{model['version']}`")
        st.markdown(f"**Description:** {model['description']}")

        if lb:
            st.markdown("**All Metrics:**")
            metrics_df_data = {
                "Metric": ["Detection Rate", "Precision", "Severity Accuracy", "Time to Discovery (norm)"],
                "Score": [
                    f"{lb['detection_rate']*100:.1f}%",
                    f"{lb['precision']*100:.1f}%",
                    f"{lb['severity_accuracy']*100:.1f}%",
                    f"{lb['time_to_discovery']*100:.1f}",
                ]
            }
            import pandas as pd
            st.table(pd.DataFrame(metrics_df_data))
