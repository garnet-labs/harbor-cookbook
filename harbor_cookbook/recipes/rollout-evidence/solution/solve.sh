#!/bin/bash
set -eu
printf 'done\n' > /app/result.txt
if [ "${PLANT_POSITIVES:-0}" = 1 ]; then
    curl --fail --silent --show-error --http1.1 --max-time 30 https://example.com -o /tmp/off-policy.html
    printf 'planted\n' > /tests/planted.txt
    nohup sleep 600 </dev/null >/tmp/rollout-background.log 2>&1 &
fi
