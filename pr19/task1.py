"""Завдання 1. Конструктор з перевіркою."""


class Wallet:
    def __init__(self, owner, balance):
        if not str(owner).strip():
            raise ValueError("ім'я власника не може бути порожнім")
        if balance < 0:
            raise ValueError("початковий баланс не може бути від'ємним")
        self.owner = owner
        self.balance = round(balance, 2)


def try_create(owner, balance):
    try:
        wallet = Wallet(owner, balance)
    except ValueError as error:
        print(f"Не вдалося створити гаманець ({owner!r}, {balance}): {error}")
        return None
    print(f"Створено гаманець: власник {wallet.owner}, баланс {wallet.balance}")
    return wallet


if __name__ == "__main__":
    try_create("Vadym Soltys", 15000.456)  
    try_create("", 1000)                   
    try_create("Vadym Soltys", -50)         
