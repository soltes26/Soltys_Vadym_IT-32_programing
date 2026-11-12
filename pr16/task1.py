import json
import sys
from pathlib import Path

NAME = "Vadym Soltys"
GROUP = "IT-32"
BASE = Path(__file__).resolve().parent
SOURCE = BASE / "data" / "expenses.csv"
TARGET = BASE / "data" / "expenses.json"


def read_csv(path):
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(";")]
        try:
            if len(parts) != 4:
                raise ValueError("expected 4 fields")
            records.append({"date": parts[0], "category": parts[1],
                            "amount": float(parts[2]), "comment": parts[3]})
        except ValueError as error:
            print(f"warning: line {number} skipped ({error}): {line}", file=sys.stderr)
    return records


def main():
    print(f"{NAME}, {GROUP}")
    if not SOURCE.is_file():
        print(f"error: {SOURCE} not found", file=sys.stderr)
        sys.exit(1)

    records = read_csv(SOURCE)
    with TARGET.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"records: {len(records)}")
    print(f"saved: data/{TARGET.name} ({TARGET.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
