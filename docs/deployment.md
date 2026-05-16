# Deployment Guide — SC Audit Studio on Streamlit Cloud

## Prerequisites

- A GitHub account (free)
- A Streamlit Cloud account (free at share.streamlit.io)
- API keys for the LLM models you want to enable

---

## Step 1 — Prepare your GitHub Repository

1. Create a new repository on GitHub (can be public or private).
2. Upload all files from this package maintaining the folder structure:

```
your-repo/
├── streamlit_app/
│   ├── app.py
│   ├── pages/
│   │   ├── 01_Leaderboard.py
│   │   ├── 02_Comparison.py
│   │   ├── 03_Vulnerabilities.py
│   │   ├── 04_Model_Registry.py
│   │   ├── 05_Baseline_Metrics.py
│   │   └── 06_Custom_Audit.py
│   ├── data/
│   │   ├── benchmark_data.py
│   │   └── vulnerabilities.py
│   └── utils/
│       ├── llm_clients.py
│       ├── scoring.py
│       └── parser.py
├── requirements.txt
└── README.md
```

3. Do NOT commit `.env` — it contains secrets. It is already in `.gitignore`.

---

## Step 2 — Create a Streamlit Cloud App

1. Go to **https://share.streamlit.io** and sign in with GitHub.
2. Click **"New app"**.
3. Fill in:
   - **Repository:** `your-username/your-repo-name`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app/app.py`
4. Click **"Advanced settings"** — do NOT add secrets here yet.
5. Click **"Deploy"** — the app will build (first deploy takes ~2 minutes).

---

## Step 3 — Add API Keys (Secrets)

After deployment, go to your app's settings → **Secrets** tab and paste:

```toml
# Required — add only the keys you have

OPENAI_API_KEY = "sk-...your_openai_key..."
ANTHROPIC_API_KEY = "sk-ant-...your_anthropic_key..."
GOOGLE_API_KEY = "AIza...your_google_key..."
GITHUB_TOKEN = "ghp_...your_github_token..."
```

**Where to get each key:**

| Key | URL | Free Tier |
|-----|-----|-----------|
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys | No (pay-as-you-go required for GPT-4) |
| `ANTHROPIC_API_KEY` | https://console.anthropic.com/settings/keys | Yes (limited) |
| `GOOGLE_API_KEY` | https://aistudio.google.com/app/apikey | Yes (generous quota) |
| `GITHUB_TOKEN` | https://github.com/settings/tokens | Requires Copilot subscription |

After saving secrets, click **"Reboot app"** in the Streamlit Cloud dashboard.

---

## Step 4 — Verify the Deployment

1. Open your app URL (format: `https://your-username-your-repo-name-app-xxxx.streamlit.app`)
2. Navigate to **Custom Audit** in the sidebar
3. Upload a `.sol` file — models with configured keys will be enabled automatically

---

## Step 5 (Optional) — Custom Domain

Streamlit Cloud Pro supports custom domains. Go to App Settings → Custom Domain and follow the CNAME instructions.

---

## Running Locally (for development)

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Create virtual environment
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add your keys

# Start the app
streamlit run streamlit_app/app.py
# Opens at http://localhost:8501
```

---

## Cost Estimates (per full benchmark run, 15 contracts × 4 models)

| Model | Approx. Cost |
|-------|-------------|
| GPT-4 Turbo | ~$0.80–$1.20 |
| Claude 3.5 Sonnet | ~$0.40–$0.70 |
| Gemini 1.5 Pro | ~$0.05–$0.15 |
| GitHub Copilot | Included in subscription ($10–19/mo) |

Custom contract audits (single file) cost roughly 1/15th of a full benchmark run.

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: openai` | Run `pip install -r requirements.txt` |
| `OPENAI_API_KEY is not set` | Add the key to `.env` (local) or Streamlit Secrets (cloud) |
| `RateLimitError` | You've hit your API quota — wait or upgrade your plan |
| `AuthenticationError` | Key is invalid or expired — regenerate it from the provider portal |
| App doesn't reload after adding secrets | Click "Reboot app" in Streamlit Cloud dashboard |
| `.sol` file rejected | Ensure file extension is exactly `.sol` (not `.txt` renamed) |
