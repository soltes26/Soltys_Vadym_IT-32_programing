import sys
from pathlib import Path

from tabulate import tabulate

NAME = "Vadym Soltys"
GROUP = "IT-32"
EXPENSES = Path(__file__).resolve().parent / "data" / "expenses.csv"


def read_expenses(path):
    """Повертає список (категорія, сума); коментарі та порожні рядки пропускає."""
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(";")
        try:
            rows.append((parts[1].strip(), float(parts[2])))
        except (IndexError, ValueError):
            print(f"warning: line {number} skipped: {line}", file=sys.stderr)
    return rows


def main():
    print(f"{NAME}, {GROUP}")

    if not EXPENSES.is_file():
        print(f"error: {EXPENSES} not found", file=sys.stderr)
        sys.exit(1)

    stats = {}  # категорія -> [кількість, сума]
    for category, amount in read_expenses(EXPENSES):
        entry = stats.setdefault(category, [0, 0.0])
        entry[0] += 1
        entry[1] += amount

    table = [[name, count, total] for name, (count, total) in stats.items()]
    table.append([
        "TOTAL",
        sum(count for count, _ in stats.values()),
        sum(total for _, total in stats.values()),
    ])
    print(tabulate(table, headers=["category", "count", "total"],
                   tablefmt="github", floatfmt=".2f"))


if __name__ == "__main__":
    main()
