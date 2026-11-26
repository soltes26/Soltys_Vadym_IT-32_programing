"""Завдання 1. Ієрархія Person -> Student -> GroupLeader."""


class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def describe(self):
        return f"{self.name} {self.surname}"


class Student(Person):
    def __init__(self, name, surname, group):
        super().__init__(name, surname)
        self.group = group

    def describe(self):
        return f"{super().describe()}, {self.group}"


class GroupLeader(Student):
    def __init__(self, name, surname, group, phone):
        super().__init__(name, surname, group)
        self.phone = phone

    def describe(self):
        return f"{super().describe()}, group leader, {self.phone}"


# --- ДАНІ СТАРОСТИ: замініть на справжні ---
LEADER_NAME = "Name"
LEADER_SURNAME = "Surname"
LEADER_PHONE = "+380 XX XXX XX XX"
# -------------------------------------------


def main():
    me = Student("Vadym", "Soltys", "IT-32")
    leader = GroupLeader(LEADER_NAME, LEADER_SURNAME, "IT-32", LEADER_PHONE)
    print(me.describe())
    print(leader.describe())


if __name__ == "__main__":
    main()
