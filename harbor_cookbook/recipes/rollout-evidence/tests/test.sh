#!/bin/sh
set -eu
export PYTHONPATH="/tests${PYTHONPATH:+:$PYTHONPATH}"
cp /evidence/rollout-evidence.json /logs/verifier/rollout-evidence.json
exec python -m rewardkit /tests
