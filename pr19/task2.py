"""Завдання 2. Інкапсуляція: приватний атрибут __balance."""


class Wallet:
    def __init__(self, owner, balance):
        if not str(owner).strip():
            raise ValueError("ім'я власника не може бути порожнім")
        if balance < 0:
            raise ValueError("початковий баланс не може бути від'ємним")
        self.owner = owner
        self.__balance = round(balance, 2)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("сума поповнення має бути додатною")
        self.__balance = round(self.__balance + amount, 2)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("сума зняття має бути додатною")
        if amount > self.__balance:
            raise ValueError(f"недостатньо коштів: баланс {self.__balance}, потрібно {amount}")
        self.__balance = round(self.__balance - amount, 2)

    def show(self):
        return self.__balance


if __name__ == "__main__":
    wallet = Wallet("Vadym Soltys", 15000)
    wallet.deposit(500)
    wallet.withdraw(1200.50)
    print("Баланс через метод show():", wallet.show())

    try:
        wallet.withdraw(100000)
    except ValueError as error:
        print("Помилка зняття:", error)

    try:
        print(wallet.__balance)
    except AttributeError as error:
        print("Читання wallet.__balance:", error)

    print("Читання wallet._Wallet__balance:", wallet._Wallet__balance)
    wallet._Wallet__balance = -999       
    print("Після прямого запису в _Wallet__balance:", wallet.show())
