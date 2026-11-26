"""Завдання 4. Поліморфізм: різні класи без спільного предка."""
from task1 import CSV_FILE
from task2 import load_lines

# --- ЗАМІНІТЬ НА СВОЇ СУМИ ---
INCOMES = [("stipend", 2000.00), ("part-time job", 1000.00)]
TRANSFERS = [("card to card", 500.00)]
# -----------------------------


class Expense:
    kind = "expenses"

    def __init__(self, category, amount):
        self.category = category
        self.amount = amount

    def balance_change(self):
        return -self.amount


class Income:
    kind = "income"

    def __init__(self, source, amount):
        self.source = source
        self.amount = amount

    def balance_change(self):
        return self.amount


class Transfer:
    kind = "transfers"

    def __init__(self, note, amount):
        self.note = note
        self.amount = amount

    def balance_change(self):
        return 0


def build_operations():
    lines = CSV_FILE.read_text(encoding="utf-8").splitlines()
    operations = [Expense(e.category, e.amount) for e in load_lines(lines)]
    operations += [Income(source, amount) for source, amount in INCOMES]
    operations += [Transfer(note, amount) for note, amount in TRANSFERS]
    return operations


def main():
    print("Vadym Soltys, IT-32")
    totals = {"income": 0, "expenses": 0, "transfers": 0}
    for operation in build_operations():
        totals[operation.kind] += operation.balance_change()

    for kind, total in totals.items():
        print(f"{kind + ':':<10}{total:>8.2f}")
    print(f"{'balance:':<10}{sum(totals.values()):>8.2f}")


if __name__ == "__main__":
    main()
