from datetime import datetime
from pathlib import Path

EXPENSES = Path(__file__).resolve().parent / "data" / "expenses.csv"
LIMIT = 200


class Expense:
    def __init__(self, date, category, amount, comment):
        self.date = date
        self.category = category
        self.amount = amount
        self.comment = comment

    def is_big(self, limit):
        return self.amount > limit

    def describe(self):
        return f"{self.date:%d.%m.%Y} {self.category} {self.amount:.2f} ({self.comment})"


def load_expenses(path):
    """Читає файл у список об'єктів Expense (коментарі й порожні рядки пропускає)."""
    expenses = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        day, category, amount, comment = (part.strip() for part in line.split(";"))
        expenses.append(Expense(datetime.strptime(day, "%Y-%m-%d").date(),
                                category, float(amount), comment))
    return expenses


def main():
    expenses = load_expenses(EXPENSES)
    print(f"objects: {len(expenses)}")
    print(f"big expenses (amount > {LIMIT}):")
    for expense in expenses:
        if expense.is_big(LIMIT):
            print(" ", expense.describe())


if __name__ == "__main__":
    main()
