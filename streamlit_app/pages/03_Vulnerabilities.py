"""03_Vulnerabilities.py — Browse the 15 test-case dataset."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from data.vulnerabilities import VULNERABILITIES

st.set_page_config(page_title="Vulnerabilities — SC Audit Studio", page_icon="🔍", layout="wide")
st.title("🔍 Vulnerability Dataset")
st.markdown("15 hand-labelled Solidity test cases used in the benchmark.")
st.divider()

SEV_COLOR = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "⚪"}

severity_filter = st.selectbox("Filter by severity", ["All", "critical", "high", "medium", "low"])
filtered = VULNERABILITIES if severity_filter == "All" else [v for v in VULNERABILITIES if v["severity"] == severity_filter]
st.caption(f"Showing {len(filtered)} of {len(VULNERABILITIES)} cases")
st.divider()

for vuln in filtered:
    icon = SEV_COLOR.get(vuln["severity"], "⚪")
    detected_count = len(vuln.get("detected_by", []))

    with st.expander(f"{icon} [{vuln['id'].upper()}] {vuln['title']} — {vuln['severity'].upper()} · Detected by {detected_count}/4 models"):
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"**Category:** {vuln['category']}")
        c2.markdown(f"**SWC:** {vuln['swc_id']}")
        c3.markdown(f"**CWE:** {vuln['cwe_id']}")
        c4.markdown(f"**Real exploit:** {vuln['real_exploit']}")

        st.markdown(f"**Description:** {vuln['description']}")

        st.code(vuln["solidity_snippet"], language="solidity")

        if vuln.get("detected_by"):
            model_map = {"gpt-4": "GPT-4", "claude": "Claude", "gemini": "Gemini", "copilot": "Copilot"}
            detected_str = " · ".join(f"✅ {model_map.get(m, m)}" for m in vuln["detected_by"])
            all_ids = ["gpt-4", "claude", "gemini", "copilot"]
            missed = [m for m in all_ids if m not in vuln["detected_by"]]
            missed_str = " · ".join(f"❌ {model_map.get(m, m)}" for m in missed)
            st.markdown(f"**Detected:** {detected_str}")
            if missed_str:
                st.markdown(f"**Missed:** {missed_str}")
