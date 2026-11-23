import math

from task3 import EXPENSES, load_expenses


class ExpenseBook:
    def __init__(self):
        self.expenses = []

    def add(self, expense):
        self.expenses.append(expense)

    def total(self):
        return round(math.fsum(e.amount for e in self.expenses), 2)

    def by_category(self, category):
        return round(math.fsum(e.amount for e in self.expenses if e.category == category), 2)

    def categories(self):
        return sorted({e.category for e in self.expenses})

    def top(self, n):
        return sorted(self.expenses, key=lambda e: e.amount, reverse=True)[:n]


def main():
    book = ExpenseBook()
    for expense in load_expenses(EXPENSES):
        book.add(expense)

    print(f"records: {len(book.expenses)}")
    print(f"total: {book.total():.2f}")
    print("by category:")
    for category in book.categories():
        print(f"  {category:<14} {book.by_category(category):8.2f}")
    print("top 3:")
    for expense in book.top(3):
        print(" ", expense.describe())


if __name__ == "__main__":
    main()
