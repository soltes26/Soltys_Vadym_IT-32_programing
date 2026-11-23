"""Завдання 5. Деструктор __del__."""

class Wallet:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def __del__(self):
        print(f"wallet of {self.owner} deleted")


print("=== Випадок 1: del wallet (єдине посилання) ===")
wallet = Wallet("Vadym Soltys", 1000)
del wallet
print("після del wallet")

print("\n=== Випадок 2: є друге посилання ===")
wallet = Wallet("Vadym Soltys (2)", 1000)
other = wallet
del wallet
print("після del wallet: об'єкт ще живий через other, деструктор не викликано")
del other
print("після del other")

print("\n=== Випадок 3: об'єкт живе до кінця програми ===")
final = Wallet("Vadym Soltys (3)", 1000)
print("кінець програми")
