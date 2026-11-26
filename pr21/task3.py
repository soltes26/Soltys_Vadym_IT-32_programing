"""Завдання 3. Змінні класу та метод класу set_currency()."""
from task1 import CSV_FILE
from task2 import Expense as CheckedExpense
from task2 import load_lines


class Expense(CheckedExpense):
    currency = "UAH"    # спільна для всіх об'єктів
    count = 0           # кількість створених об'єктів

    def __init__(self, date, category, amount, comment=""):
        super().__init__(date, category, amount, comment)
        Expense.count += 1

    @classmethod
    def set_currency(cls, code):
        cls.currency = code

    def describe(self):
        return f"{super().describe():<45} {self.currency}"


def main():
    print("Vadym Soltys, IT-32")
    lines = CSV_FILE.read_text(encoding="utf-8").splitlines()
    expenses = load_lines(lines, Expense)
    print("created objects:", Expense.count)

    print("--- currency:", Expense.currency)
    for expense in expenses[:3]:
        print(expense.describe())

    Expense.set_currency("USD")   # змінюється лише позначення, суми не перераховуються
    print("--- after Expense.set_currency('USD')")
    for expense in expenses[:3]:
        print(expense.describe())
    print("all objects use USD:", all(e.currency == "USD" for e in expenses))


if __name__ == "__main__":
    main()
