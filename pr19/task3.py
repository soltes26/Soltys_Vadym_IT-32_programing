"""Завдання 3. Властивості @property."""


class Wallet:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        if not str(value).strip():
            raise ValueError("ім'я власника не може бути порожнім")
        self.__owner = value

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance can not be negative")
        self.__balance = round(value, 2)

    @property
    def is_empty(self):
        return self.__balance == 0


if __name__ == "__main__":
    wallet = Wallet("Vadym Soltys", 1500)
    print(wallet.balance)
    wallet.balance = 1200.555
    print(wallet.balance)
    print("is_empty:", wallet.is_empty)

    try:
        wallet.balance = -10
    except ValueError as error:
        print("ValueError:", error)

    try:
        wallet.owner = "   "
    except ValueError as error:
        print("ValueError:", error)

    try:
        wallet.is_empty = True
    except AttributeError as error:
        print("AttributeError:", error)

    wallet.balance = 0
    print("is_empty після обнулення:", wallet.is_empty)
