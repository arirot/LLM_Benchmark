"""
llm_clients.py
Wrappers for each LLM provider API.
Set the corresponding environment variables in .env before using.
"""

import os
import time
from typing import Optional

# Load env vars from .env if running locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional; Streamlit Cloud uses st.secrets instead


AUDIT_PROMPT_TEMPLATE = """You are a senior smart contract security auditor specializing in Solidity and EVM-compatible blockchains.

Audit the following Solidity contract for security vulnerabilities. For each finding, provide:
1. Vulnerability name
2. Severity: critical / high / medium / low
3. Affected line number (approximate)
4. Brief description (1-2 sentences)
5. Recommended fix (1-2 sentences)

Format each finding as:
FINDING: <name>
SEVERITY: <level>
LINE: <number>
DESCRIPTION: <text>
FIX: <text>
---

Contract to audit:
```solidity
{contract_code}
```

Provide only genuine findings. Do not hallucinate vulnerabilities that are not present."""


# ---------------------------------------------------------------------------
# OpenAI — GPT-4 Turbo
# ---------------------------------------------------------------------------

def audit_with_gpt4(contract_code: str) -> dict:
    """
    Run a vulnerability audit using GPT-4 Turbo.
    Requires: OPENAI_API_KEY in environment.
    Get your key: https://platform.openai.com/api-keys
    """
    try:
        import openai
    except ImportError:
        raise ImportError("Run: pip install openai>=1.30.0")

    api_key = os.getenv("OPENAI_API_KEY") or _get_streamlit_secret("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. "
            "Get your key at https://platform.openai.com/api-keys"
        )

    client = openai.OpenAI(api_key=api_key)
    prompt = AUDIT_PROMPT_TEMPLATE.format(contract_code=contract_code)

    start = time.time()
    response = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.1,
    )
    elapsed = time.time() - start
    text = response.choices[0].message.content or ""

    return {
        "model_id": "gpt-4",
        "model_name": "GPT-4 Turbo",
        "color": "#10A37F",
        "raw_response": text,
        "time_seconds": round(elapsed, 2),
        "input_tokens": response.usage.prompt_tokens if response.usage else None,
        "output_tokens": response.usage.completion_tokens if response.usage else None,
    }


# ---------------------------------------------------------------------------
# Anthropic — Claude 3.5 Sonnet
# ---------------------------------------------------------------------------

def audit_with_claude(contract_code: str) -> dict:
    """
    Run a vulnerability audit using Claude 3.5 Sonnet.
    Requires: ANTHROPIC_API_KEY in environment.
    Get your key: https://console.anthropic.com/settings/keys
    """
    try:
        import anthropic
    except ImportError:
        raise ImportError("Run: pip install anthropic>=0.28.0")

    api_key = os.getenv("ANTHROPIC_API_KEY") or _get_streamlit_secret("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY is not set. "
            "Get your key at https://console.anthropic.com/settings/keys"
        )

    client = anthropic.Anthropic(api_key=api_key)
    prompt = AUDIT_PROMPT_TEMPLATE.format(contract_code=contract_code)

    start = time.time()
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    elapsed = time.time() - start
    text = message.content[0].text if message.content else ""

    return {
        "model_id": "claude",
        "model_name": "Claude 3.5 Sonnet",
        "color": "#D97706",
        "raw_response": text,
        "time_seconds": round(elapsed, 2),
        "input_tokens": message.usage.input_tokens if message.usage else None,
        "output_tokens": message.usage.output_tokens if message.usage else None,
    }


# ---------------------------------------------------------------------------
# Google — Gemini 1.5 Pro
# ---------------------------------------------------------------------------

def audit_with_gemini(contract_code: str) -> dict:
    """
    Run a vulnerability audit using Gemini 1.5 Pro.
    Requires: GOOGLE_API_KEY in environment.
    Get your key: https://aistudio.google.com/app/apikey
    """
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError("Run: pip install google-generativeai>=0.7.0")

    api_key = os.getenv("GOOGLE_API_KEY") or _get_streamlit_secret("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not set. "
            "Get your key at https://aistudio.google.com/app/apikey"
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    prompt = AUDIT_PROMPT_TEMPLATE.format(contract_code=contract_code)

    start = time.time()
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=2000,
            temperature=0.1,
        ),
    )
    elapsed = time.time() - start
    text = response.text if hasattr(response, "text") else ""

    return {
        "model_id": "gemini",
        "model_name": "Gemini 1.5 Pro",
        "color": "#3B82F6",
        "raw_response": text,
        "time_seconds": round(elapsed, 2),
        "input_tokens": None,   # Gemini SDK doesn't expose token counts easily
        "output_tokens": None,
    }


# ---------------------------------------------------------------------------
# GitHub Copilot (via OpenAI-compatible Azure endpoint)
# ---------------------------------------------------------------------------

def audit_with_copilot(contract_code: str) -> dict:
    """
    Run a vulnerability audit using GitHub Copilot (GPT-4o powered).
    Requires: GITHUB_TOKEN in environment.
    Get your token: https://github.com/settings/tokens
    Note: Requires an active GitHub Copilot subscription.
    """
    try:
        import openai
    except ImportError:
        raise ImportError("Run: pip install openai>=1.30.0")

    github_token = os.getenv("GITHUB_TOKEN") or _get_streamlit_secret("GITHUB_TOKEN")
    if not github_token:
        raise ValueError(
            "GITHUB_TOKEN is not set. "
            "Get your token at https://github.com/settings/tokens"
        )

    # GitHub Copilot exposes an OpenAI-compatible endpoint
    endpoint = os.getenv("GITHUB_COPILOT_ENDPOINT", "https://api.githubcopilot.com")
    client = openai.OpenAI(
        base_url=endpoint,
        api_key=github_token,
    )
    prompt = AUDIT_PROMPT_TEMPLATE.format(contract_code=contract_code)

    start = time.time()
    response = client.chat.completions.create(
        model="gpt-4o",  # Copilot's model identifier
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.1,
    )
    elapsed = time.time() - start
    text = response.choices[0].message.content or ""

    return {
        "model_id": "copilot",
        "model_name": "GitHub Copilot",
        "color": "#8B5CF6",
        "raw_response": text,
        "time_seconds": round(elapsed, 2),
        "input_tokens": response.usage.prompt_tokens if response.usage else None,
        "output_tokens": response.usage.completion_tokens if response.usage else None,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_streamlit_secret(key: str) -> Optional[str]:
    """Safely read from st.secrets (Streamlit Cloud) without hard-failing."""
    try:
        import streamlit as st
        return st.secrets.get(key)
    except Exception:
        return None


def get_available_models() -> list[str]:
    """Return model IDs whose API keys are currently configured."""
    available = []
    if os.getenv("OPENAI_API_KEY") or _get_streamlit_secret("OPENAI_API_KEY"):
        available.append("gpt-4")
    if os.getenv("ANTHROPIC_API_KEY") or _get_streamlit_secret("ANTHROPIC_API_KEY"):
        available.append("claude")
    if os.getenv("GOOGLE_API_KEY") or _get_streamlit_secret("GOOGLE_API_KEY"):
        available.append("gemini")
    if os.getenv("GITHUB_TOKEN") or _get_streamlit_secret("GITHUB_TOKEN"):
        available.append("copilot")
    return available


MODEL_AUDIT_FN = {
    "gpt-4":   audit_with_gpt4,
    "claude":  audit_with_claude,
    "gemini":  audit_with_gemini,
    "copilot": audit_with_copilot,
}
