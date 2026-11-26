"""Завдання 1. Альтернативні конструктори (@classmethod)."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
CSV_FILE = DATA / "expenses.csv"
JSON_FILE = DATA / "expenses.json"


class Expense:
    def __init__(self, date, category, amount, comment=""):
        self.date = date
        self.category = category
        self.amount = amount
        self.comment = comment

    @classmethod
    def from_csv_line(cls, line):
        date, category, amount, comment = line.strip().split(";")
        return cls(date, category, float(amount), comment)

    @classmethod
    def from_dict(cls, data):
        return cls(data["date"], data["category"], float(data["amount"]),
                   data.get("comment", ""))

    @classmethod
    def from_input(cls):
        date = input("date (YYYY-MM-DD): ").strip()
        category = input("category: ").strip()
        amount = float(input("amount: "))
        comment = input("comment: ").strip()
        return cls(date, category, amount, comment)

    def describe(self):
        return f"{self.date} {self.category:<14}{self.amount:>8.2f}  {self.comment}"


def load_csv(path):
    expenses = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            expenses.append(Expense.from_csv_line(line))
    return expenses


def load_json(path):
    with path.open(encoding="utf-8") as file:
        return [Expense.from_dict(record) for record in json.load(file)]


def main():
    print("Vadym Soltys, IT-32")
    from_csv = load_csv(CSV_FILE)
    from_json = load_json(JSON_FILE)
    for expense in from_csv:
        print(expense.describe())
    print(f"from CSV:  {len(from_csv)} expenses")
    print(f"from JSON: {len(from_json)} expenses")
    # vars() повертає словник атрибутів об'єкта
    same = [vars(e) for e in from_csv] == [vars(e) for e in from_json]
    print("same data:", same)

    print("--- new expense from keyboard")
    try:
        print(Expense.from_input().describe())
    except ValueError as error:
        print("error:", error)
    except EOFError:
        print("\ninput cancelled")


if __name__ == "__main__":
    main()
