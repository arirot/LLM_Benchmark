"""
parser.py
Parse raw LLM audit responses into structured Finding objects.
"""

import re
from dataclasses import dataclass, field
from typing import Optional

SEVERITY_LEVELS = {"critical", "high", "medium", "low"}


@dataclass
class Finding:
    title: str
    severity: str         # critical | high | medium | low
    line: Optional[int]
    description: str
    recommendation: str
    raw_block: str = field(repr=False, default="")

    def severity_is_valid(self) -> bool:
        return self.severity.lower() in SEVERITY_LEVELS


def parse_findings(raw_response: str) -> list[Finding]:
    """
    Parse a structured LLM audit response into a list of Finding objects.

    Expected block format (enforced by AUDIT_PROMPT_TEMPLATE):
        FINDING: <name>
        SEVERITY: <level>
        LINE: <number>
        DESCRIPTION: <text>
        FIX: <text>
        ---
    """
    findings: list[Finding] = []

    # Split on --- separator or double-newline between findings
    blocks = re.split(r"\n---+\n?", raw_response.strip())

    for block in blocks:
        block = block.strip()
        if not block or "FINDING:" not in block.upper():
            continue

        def _extract(label: str) -> str:
            pattern = rf"(?i)^{label}:\s*(.+?)(?=\n[A-Z]+:|$)"
            match = re.search(pattern, block, re.MULTILINE | re.DOTALL)
            return match.group(1).strip() if match else ""

        title       = _extract("FINDING")
        severity    = _extract("SEVERITY").lower()
        line_str    = _extract("LINE")
        description = _extract("DESCRIPTION")
        fix         = _extract("FIX")

        if not title:
            continue

        line: Optional[int] = None
        try:
            digits = re.search(r"\d+", line_str)
            if digits:
                line = int(digits.group())
        except ValueError:
            pass

        # Normalise severity
        if severity not in SEVERITY_LEVELS:
            # Try to guess from text
            for lvl in SEVERITY_LEVELS:
                if lvl in severity:
                    severity = lvl
                    break
            else:
                severity = "medium"  # safe default

        findings.append(Finding(
            title=title,
            severity=severity,
            line=line,
            description=description,
            recommendation=fix,
            raw_block=block,
        ))

    return findings


def count_severity(findings: list[Finding]) -> dict[str, int]:
    counts = {lvl: 0 for lvl in SEVERITY_LEVELS}
    for f in findings:
        lvl = f.severity if f.severity in SEVERITY_LEVELS else "medium"
        counts[lvl] += 1
    return counts
