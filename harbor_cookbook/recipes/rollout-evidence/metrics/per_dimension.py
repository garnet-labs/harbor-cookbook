"""Report coverage and cleanliness separately; unknown is never clean."""

import argparse
import json
from pathlib import Path


def aggregate(rewards):
    rows = [row for row in rewards if row is not None]
    output = {}
    for check in ("off_policy_host", "tests_write", "background_proc"):
        known = sum(row.get(f"{check}_known", 0) for row in rows)
        clean = sum(row.get(f"{check}_clean", 0) for row in rows)
        output[f"{check}_known"] = known / len(rows) if rows else 0
        output[f"{check}_clean"] = clean / len(rows) if rows else 0
        if known:
            output[f"{check}_clean_given_known"] = clean / known
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True)
    parser.add_argument("-o", required=True)
    args = parser.parse_args()
    rows = [
        json.loads(line)
        for line in Path(args.i).read_text().splitlines()
        if line.strip()
    ]
    Path(args.o).write_text(json.dumps(aggregate(rows)))


if __name__ == "__main__":
    main()
