"""Завдання 2. Статичні методи-перевірки (@staticmethod)."""
import math
from datetime import datetime

from task1 import CSV_FILE
from task1 import Expense as BaseExpense

# Навмисно некоректні рядки для перевірки
BAD_LINES = [
    "2026-02-30;food;50.00;wrong day",
    "08.11.2026;food;50.00;wrong format",
    "2026-11-08;food;abc;not a number",
    "2026-11-08;food;-20.00;negative amount",
    "2026-11-08;food",
]


class Expense(BaseExpense):
    @staticmethod
    def is_valid_date(text):
        try:
            parsed = datetime.strptime(text, "%Y-%m-%d")
        except (TypeError, ValueError):
            return False
        # strptime приймає і "2026-1-5", тому порівнюємо з точним форматом
        return parsed.strftime("%Y-%m-%d") == text

    @staticmethod
    def is_valid_amount(value):
        try:
            number = float(value)
        except (TypeError, ValueError):
            return False
        return math.isfinite(number) and number > 0

    @classmethod
    def from_csv_line(cls, line):
        parts = line.strip().split(";")
        if len(parts) != 4:
            raise ValueError("expected 4 fields")
        date, _, amount, _ = parts
        if not cls.is_valid_date(date):
            raise ValueError(f"invalid date {date!r}")
        if not cls.is_valid_amount(amount):
            raise ValueError(f"invalid amount {amount!r}")
        return super().from_csv_line(line)


def load_lines(lines, cls=Expense):
    """Створює витрати з рядків CSV; некоректні рядки пропускає з повідомленням."""
    expenses = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            expenses.append(cls.from_csv_line(line))
        except ValueError as error:
            print(f"skipped: {line} ({error})")
    return expenses


def main():
    print("Vadym Soltys, IT-32")
    print("--- calls without an object")
    for date in ("2026-11-08", "2026-02-30", "08.11.2026"):
        print(f"is_valid_date({date!r}): {Expense.is_valid_date(date)}")
    for value in ("85.50", "abc", -5):
        print(f"is_valid_amount({value!r}): {Expense.is_valid_amount(value)}")

    lines = CSV_FILE.read_text(encoding="utf-8").splitlines()
    print("--- my file")
    print(f"loaded: {len(load_lines(lines))} expenses")
    print("--- bad lines")
    print(f"loaded: {len(load_lines(BAD_LINES))} expenses")


if __name__ == "__main__":
    main()
