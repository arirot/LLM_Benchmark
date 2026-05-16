# SC Audit Studio — LLM Benchmark

> Benchmarking GPT-4, Claude 3.5, Gemini 1.5 Pro, and GitHub Copilot on smart contract vulnerability detection.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What This Does

SC Audit Studio evaluates how well leading large language models detect vulnerabilities in Solidity smart contracts. It provides:

- **Leaderboard** — composite score ranking across 4 models
- **Comparison Matrix** — side-by-side metric breakdown (detection rate, precision, time-to-discovery, severity accuracy)
- **Vulnerability Dataset** — 15 hand-labelled Solidity test cases spanning reentrancy, integer overflow, access control, flash loan oracles, and more
- **Custom Contract Audit** — upload any `.sol` file and run it through all 4 models simultaneously
- **Baseline Methodology** — explains how scores are calibrated against a human expert auditor and static analysis tools

---

## Repository Structure

```
sc-audit-studio/
├── streamlit_app/
│   ├── app.py                  # Main Streamlit entry point
│   ├── pages/
│   │   ├── 01_Leaderboard.py
│   │   ├── 02_Comparison.py
│   │   ├── 03_Vulnerabilities.py
│   │   ├── 04_Model_Registry.py
│   │   ├── 05_Baseline_Metrics.py
│   │   └── 06_Custom_Audit.py
│   ├── data/
│   │   ├── benchmark_data.py   # All in-memory benchmark results
│   │   └── vulnerabilities.py  # 15 test case definitions
│   └── utils/
│       ├── llm_clients.py      # API wrappers for each model
│       ├── scoring.py          # Composite score calculation
│       └── parser.py          # Response parser / finding extractor
├── .env.example                # Required environment variables
├── requirements.txt            # Python dependencies
├── .github/
│   └── workflows/
│       └── deploy.yml          # Optional CI/CD for Streamlit Cloud
└── README.md
```

---

## Scoring Methodology

| Metric | Weight | Formula |
|--------|--------|---------|
| Detection Rate | **40%** | TP / (TP + FN) |
| Precision | **25%** | TP / (TP + FP) |
| Severity Accuracy | **20%** | Correct Labels / TP |
| Time to Discovery | **15%** | Normalized 0–1 (lower time → higher score) |

**Composite Score** = 0.40 × DetectionRate + 0.25 × Precision + 0.15 × TimeToDiscovery + 0.20 × SeverityAccuracy

Reference points:
- Human expert auditor: **0.86** (ceiling)
- Slither + Mythril static analysis: **0.55** (floor)
- Random classifier: **0.32** (null baseline)

---

## Benchmark Results (May 2025)

| Rank | Model | Score | Detection | Precision | Sev. Accuracy |
|------|-------|-------|-----------|-----------|---------------|
| 1 | Claude 3.5 Sonnet | **0.834** | 87% | 84% | 89% |
| 2 | GPT-4 Turbo | 0.793 | 81% | 78% | 83% |
| 3 | Gemini 1.5 Pro | 0.772 | 79% | 74% | 77% |
| 4 | GitHub Copilot | 0.706 | 68% | 71% | 70% |

---

## Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/sc-audit-studio.git
cd sc-audit-studio

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up API keys
cp .env.example .env
# Edit .env with your actual API keys (see API Keys section below)

# 5. Run the app
streamlit run streamlit_app/app.py
```

The app will open at `http://localhost:8501`.

---

## API Keys Required

See `.env.example` for all required variables. Each key must be obtained from the respective provider's developer portal.

| Model | Provider | Key Variable | Where to Get It |
|-------|----------|-------------|-----------------|
| GPT-4 Turbo | OpenAI | `OPENAI_API_KEY` | platform.openai.com/api-keys |
| Claude 3.5 Sonnet | Anthropic | `ANTHROPIC_API_KEY` | console.anthropic.com/settings/keys |
| Gemini 1.5 Pro | Google | `GOOGLE_API_KEY` | aistudio.google.com/app/apikey |
| GitHub Copilot | GitHub / Azure | `GITHUB_TOKEN` | github.com/settings/tokens |

> **Important:** Never commit `.env` to version control. It is listed in `.gitignore`.

---

## Deploying to Streamlit Cloud (Free)

See `docs/deployment.md` for full step-by-step instructions.

**Summary:**
1. Push this repo to GitHub (must be public, or private with Streamlit Cloud Pro)
2. Go to share.streamlit.io → "New app"
3. Select your repo, branch `main`, entry point `streamlit_app/app.py`
4. Add API keys in the Secrets panel (TOML format)
5. Click Deploy

---

## License

MIT — free to use, modify, and distribute.
