"""Завдання 3. Види витрат: наслідування та перевизначення monthly_cost()."""
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "expenses.csv"

# Скільки разів на місяць повторюється витрата та на скількох людей вона ділиться
BUS_TIMES = 40          # 2 поїздки x 20 навчальних днів
METRO_TIMES = 8         # 2 поїздки на тиждень x 4 тижні
GROCERIES_PEOPLE = 2
CINEMA_PEOPLE = 2


class Expense:
    def __init__(self, date, category, amount):
        self.date = date
        self.category = category
        self.amount = amount

    def monthly_cost(self):
        return self.amount


class RecurringExpense(Expense):
    def __init__(self, date, category, amount, times_per_month):
        super().__init__(date, category, amount)
        self.times_per_month = times_per_month

    def monthly_cost(self):
        return super().monthly_cost() * self.times_per_month


class SharedExpense(Expense):
    def __init__(self, date, category, amount, people):
        if people < 1:
            raise ValueError("people must be at least 1")
        super().__init__(date, category, amount)
        self.people = people

    def monthly_cost(self):
        return super().monthly_cost() / self.people


def load_records(path):
    """Повертає словник {(дата, опис): (дата, категорія, сума)} з файлу витрат."""
    records = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        date, category, amount, description = line.split(";")
        records[date, description] = (date, category, float(amount))
    return records


def build_expenses():
    records = load_records(DATA)
    return [
        RecurringExpense(*records["2026-11-02", "bus"], times_per_month=BUS_TIMES),
        RecurringExpense(*records["2026-11-05", "metro"], times_per_month=METRO_TIMES),
        SharedExpense(*records["2026-11-06", "groceries"], people=GROCERIES_PEOPLE),
        SharedExpense(*records["2026-11-04", "cinema"], people=CINEMA_PEOPLE),
    ]


def print_report(expenses):
    """Друкує витрати та повертає загальну місячну вартість."""
    print(f"{'date':<12}{'category':<15}{'kind':<18}{'amount':>9}{'monthly':>10}")
    print("-" * 64)
    total = 0
    for expense in expenses:
        cost = expense.monthly_cost()
        total += cost
        print(f"{expense.date:<12}{expense.category:<15}{type(expense).__name__:<18}"
              f"{expense.amount:>9.2f}{cost:>10.2f}")
    print("-" * 64)
    print(f"{'total monthly cost':<54}{total:>10.2f}")
    return total


def main():
    print("Vadym Soltys, IT-32")
    print_report(build_expenses())


if __name__ == "__main__":
    main()
