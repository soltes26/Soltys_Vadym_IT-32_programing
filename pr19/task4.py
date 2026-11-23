"""Завдання 4. Гаманець і витрати з data/expenses.csv."""
import csv

OWNER = "Vadym Soltys"
BUDGET = 15000


class Wallet:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance can not be negative")
        self.__balance = round(value, 2)

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("недостатньо коштів")
        self.balance = self.balance - amount


def load_expenses(path):
    with open(path, encoding="utf-8", newline="") as file:
        return [(row["date"], row["description"], float(row["amount"]))
                for row in csv.DictReader(file)]


def process(wallet, expenses):
    total = 0
    for date, description, amount in expenses:
        try:
            wallet.withdraw(amount)
        except ValueError:
            print(f"Зупинка: на витрату «{description}» ({date}, {amount:.2f}) "
                  f"бракує коштів, залишок {wallet.balance:.2f}")
            return total, False
        total += amount
        print(f"{date}  {description:<22} -{amount:>9.2f}   залишок {wallet.balance:>9.2f}")
    return total, True


if __name__ == "__main__":
    expenses = load_expenses("data/expenses.csv")
    print(f"Сума всіх витрат: {sum(a for _, _, a in expenses):.2f}")

    print(f"\n--- Бюджет {BUDGET} ---")
    wallet = Wallet(OWNER, BUDGET)
    total, ok = process(wallet, expenses)
    print(f"Оброблено повністю: {ok}; списано {total:.2f}; залишок {wallet.balance:.2f}")
    print(f"Перевірка: {BUDGET} - {total:.2f} = {BUDGET - total:.2f}")

    print("\n--- Недостатній бюджет 8000 ---")
    small = Wallet(OWNER, 8000)
    process(small, expenses)
