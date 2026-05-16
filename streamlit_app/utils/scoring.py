"""
scoring.py
Composite score calculation and normalisation utilities.
"""


WEIGHTS = {
    "detection_rate": 0.40,
    "precision":      0.25,
    "severity_accuracy": 0.20,
    "time_to_discovery": 0.15,
}

TTD_MIN_SECONDS = 5.0   # fastest observed (normalised to 1.0)
TTD_MAX_SECONDS = 60.0  # slowest observed (normalised to 0.0)


def normalise_ttd(seconds: float) -> float:
    """Convert raw time-to-discovery (seconds) to 0-1 score (higher = faster)."""
    clamped = max(TTD_MIN_SECONDS, min(TTD_MAX_SECONDS, seconds))
    return 1.0 - (clamped - TTD_MIN_SECONDS) / (TTD_MAX_SECONDS - TTD_MIN_SECONDS)


def composite_score(
    detection_rate: float,
    precision: float,
    severity_accuracy: float,
    ttd_norm: float,
) -> float:
    """
    Compute the weighted composite benchmark score.

    Args:
        detection_rate:    TP / (TP + FN)  — 0 to 1
        precision:         TP / (TP + FP)  — 0 to 1
        severity_accuracy: correct_labels / TP  — 0 to 1
        ttd_norm:          normalised time-to-discovery  — 0 to 1 (higher = faster)

    Returns:
        Composite score in [0, 1].
    """
    score = (
        WEIGHTS["detection_rate"]     * detection_rate
        + WEIGHTS["precision"]        * precision
        + WEIGHTS["severity_accuracy"] * severity_accuracy
        + WEIGHTS["time_to_discovery"] * ttd_norm
    )
    return round(min(1.0, max(0.0, score)), 3)


def score_from_findings(
    total_vulnerabilities: int,
    true_positives: int,
    false_positives: int,
    correctly_labelled_severity: int,
    elapsed_seconds: float,
) -> dict:
    """
    Compute all metrics from raw finding counts.

    Returns a dict with detection_rate, precision, severity_accuracy,
    time_to_discovery (raw + norm), and composite_score.
    """
    fn = total_vulnerabilities - true_positives
    detection_rate = true_positives / (true_positives + fn) if (true_positives + fn) > 0 else 0.0
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    sev_acc = correctly_labelled_severity / true_positives if true_positives > 0 else 0.0
    ttd_norm = normalise_ttd(elapsed_seconds)

    return {
        "detection_rate": round(detection_rate, 4),
        "precision": round(precision, 4),
        "severity_accuracy": round(sev_acc, 4),
        "time_to_discovery_seconds": round(elapsed_seconds, 2),
        "time_to_discovery_norm": round(ttd_norm, 4),
        "composite_score": composite_score(detection_rate, precision, sev_acc, ttd_norm),
    }
