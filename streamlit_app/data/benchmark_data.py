"""
benchmark_data.py
All benchmark results stored in memory.
Composite score = 0.40*detection + 0.25*precision + 0.15*ttd_norm + 0.20*severity
"""

MODELS = [
    {
        "id": "gpt-4",
        "name": "GPT-4",
        "full_name": "GPT-4 Turbo",
        "version": "gpt-4-turbo-2024-04-09",
        "provider": "OpenAI",
        "context_window": 128_000,
        "color": "#10A37F",
        "description": "OpenAI flagship. Strong reasoning, broad security training.",
    },
    {
        "id": "claude",
        "name": "Claude",
        "full_name": "Claude 3.5 Sonnet",
        "version": "claude-3-5-sonnet-20241022",
        "provider": "Anthropic",
        "context_window": 200_000,
        "color": "#D97706",
        "description": "Dedicated vulnerability research capability; 200K context.",
    },
    {
        "id": "gemini",
        "name": "Gemini",
        "full_name": "Gemini 1.5 Pro",
        "version": "gemini-1.5-pro-latest",
        "provider": "Google",
        "context_window": 1_000_000,
        "color": "#3B82F6",
        "description": "Largest context window — entire codebase in one pass.",
    },
    {
        "id": "copilot",
        "name": "Copilot",
        "full_name": "GitHub Copilot",
        "version": "gpt-4o (Copilot-powered)",
        "provider": "GitHub / OpenAI",
        "context_window": 64_000,
        "color": "#8B5CF6",
        "description": "Inline code assistant evaluated via Copilot Chat audit mode.",
    },
]

LEADERBOARD = [
    {
        "rank": 1,
        "model_id": "claude",
        "model_name": "Claude 3.5 Sonnet",
        "composite_score": 0.834,
        "detection_rate": 0.87,
        "precision": 0.84,
        "time_to_discovery": 0.65,   # normalized 0-1 (higher = faster)
        "severity_accuracy": 0.89,
        "color": "#D97706",
    },
    {
        "rank": 2,
        "model_id": "gpt-4",
        "model_name": "GPT-4 Turbo",
        "composite_score": 0.793,
        "detection_rate": 0.81,
        "precision": 0.78,
        "time_to_discovery": 0.72,
        "severity_accuracy": 0.83,
        "color": "#10A37F",
    },
    {
        "rank": 3,
        "model_id": "gemini",
        "model_name": "Gemini 1.5 Pro",
        "composite_score": 0.772,
        "detection_rate": 0.79,
        "precision": 0.74,
        "time_to_discovery": 0.78,
        "severity_accuracy": 0.77,
        "color": "#3B82F6",
    },
    {
        "rank": 4,
        "model_id": "copilot",
        "model_name": "GitHub Copilot",
        "composite_score": 0.706,
        "detection_rate": 0.68,
        "precision": 0.71,
        "time_to_discovery": 0.88,   # fastest TTD
        "severity_accuracy": 0.70,
        "color": "#8B5CF6",
    },
]

CATEGORY_BREAKDOWN = {
    "Arithmetic":       {"gpt-4": 95, "claude": 98, "gemini": 92, "copilot": 88},
    "Control Flow":     {"gpt-4": 90, "claude": 95, "gemini": 86, "copilot": 80},
    "Access Control":   {"gpt-4": 88, "claude": 94, "gemini": 85, "copilot": 75},
    "Authentication":   {"gpt-4": 85, "claude": 91, "gemini": 82, "copilot": 78},
    "Error Handling":   {"gpt-4": 83, "claude": 89, "gemini": 79, "copilot": 70},
    "DeFi / Oracle":    {"gpt-4": 72, "claude": 82, "gemini": 68, "copilot": 45},
    "Proxy Pattern":    {"gpt-4": 65, "claude": 78, "gemini": 60, "copilot": 38},
    "MEV / Ordering":   {"gpt-4": 60, "claude": 72, "gemini": 55, "copilot": 42},
}

BASELINE = {
    "human_expert": 0.860,
    "static_analysis": 0.550,  # Slither + Mythril defaults
    "random_classifier": 0.320,
    "weight_detection": 0.40,
    "weight_precision": 0.25,
    "weight_severity": 0.20,
    "weight_ttd": 0.15,
}
