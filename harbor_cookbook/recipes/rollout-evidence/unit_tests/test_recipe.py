import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RECIPE = Path(__file__).resolve().parents[1]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("state", "known", "clean"),
    [
        ("observed", 1, 0),
        ("not_observed_within_scope", 1, 1),
        ("unknown", 0, 0),
    ],
)
def test_rewardkit_dimensions(tmp_path, state, known, clean):
    evidence = tmp_path / "evidence.json"
    evidence.write_text(
        json.dumps(
            {
                "checks": {
                    name: {"state": state}
                    for name in ("tests_write", "off_policy_host", "background_proc")
                }
            }
        )
    )
    output = tmp_path / "reward.json"
    env = {
        **os.environ,
        "PYTHONPATH": str(RECIPE / "tests"),
        "ROLLOUT_EVIDENCE_PATH": str(evidence),
    }
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "rewardkit",
            str(RECIPE / "tests"),
            "--workspace",
            str(tmp_path),
            "--output",
            str(output),
        ],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    rewards = json.loads(output.read_text())
    assert len(rewards) == 6
    for name in ("off_policy_host", "tests_write", "background_proc"):
        assert rewards[name + "_known"] == known
        assert rewards[name + "_clean"] == clean


@pytest.mark.parametrize("content", [None, "bad-json", "{}", '{"checks":null}'])
def test_missing_or_invalid_evidence_is_unknown(tmp_path, monkeypatch, content):
    evidence = tmp_path / "evidence.json"
    if content is not None:
        evidence.write_text(content)
    monkeypatch.setenv("ROLLOUT_EVIDENCE_PATH", str(evidence))
    module = load(RECIPE / "tests/evidence_score.py")
    assert module.score("tests_write", "known") == 0
    assert module.score("tests_write", "clean") == 0


def test_metrics_keep_unknown_in_coverage():
    module = load(RECIPE / "metrics/per_dimension.py")
    metrics = module.aggregate(
        [
            {"tests_write_known": 1, "tests_write_clean": 1},
            {"tests_write_known": 0, "tests_write_clean": 0},
        ]
    )
    assert metrics["tests_write_known"] == 0.5
    assert metrics["tests_write_clean"] == 0.5
    assert metrics["tests_write_clean_given_known"] == 1
    assert "off_policy_host_clean_given_known" not in metrics
