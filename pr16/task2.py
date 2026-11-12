import json
import sys
from datetime import date
from pathlib import Path

NAME = "Vadym Soltys"
GROUP = "IT-32"
BASE = Path(__file__).resolve().parent
SOURCE = BASE / "data" / "expenses.json"
TARGET = BASE / "data" / "expenses_updated.json"
MIN_AMOUNT = 10


def main():
    print(f"{NAME}, {GROUP}")
    try:
        with SOURCE.open(encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        print(f"error: {SOURCE} not found (run task1.py first)", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as error:
        print(f"error: {SOURCE.name} is not valid JSON (line {error.lineno})", file=sys.stderr)
        sys.exit(1)

    before = len(records)
    records.append({
        "date": date.today().isoformat(),
        "category": "study",
        "amount": 120.0,
        "comment": "python book",
    })
    kept = [r for r in records if r["amount"] >= MIN_AMOUNT]
    removed = len(records) - len(kept)

    with TARGET.open("w", encoding="utf-8") as f:
        json.dump(kept, f, indent=2, ensure_ascii=False)

    print(f"read: {before} records")
    print("added: 1")
    print(f"removed: {removed} (amount < {MIN_AMOUNT})")
    print(f"saved: data/{TARGET.name} ({len(kept)} records)")


if __name__ == "__main__":
    main()
