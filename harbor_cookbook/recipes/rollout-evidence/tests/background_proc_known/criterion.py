from pathlib import Path

from evidence_score import score
from rewardkit import criterion


@criterion
def evidence_dimension(workspace: Path) -> int:
    return score("background_proc", "known")
