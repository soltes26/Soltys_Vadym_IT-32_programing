"""Завдання 4. Новий вид витрати без змін базового класу та циклу."""
from task3 import Expense, build_expenses, print_report

# Річна підписка: замініть дату, категорію та суму на свої
SUBSCRIPTION = ("2026-11-01", "subscription", 1200.00)


class YearlyExpense(Expense):
    def monthly_cost(self):
        return super().monthly_cost() / 12


def main():
    print("Vadym Soltys, IT-32")
    expenses = build_expenses()
    expenses.append(YearlyExpense(*SUBSCRIPTION))
    print_report(expenses)


if __name__ == "__main__":
    main()
