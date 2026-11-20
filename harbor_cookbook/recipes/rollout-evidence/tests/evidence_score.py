"""Numeric companions to tri-state evidence, never a substitute for its scope."""

import json
import os
from pathlib import Path


def score(check, dimension):
    try:
        path = Path(
            os.environ.get("ROLLOUT_EVIDENCE_PATH", "/evidence/rollout-evidence.json")
        )
        evidence = json.loads(path.read_text())
        state = evidence["checks"][check]["state"]
    except (OSError, ValueError, KeyError, TypeError):
        state = "unknown"
    if dimension == "known":
        return int(state in ("observed", "not_observed_within_scope"))
    return int(state == "not_observed_within_scope")
