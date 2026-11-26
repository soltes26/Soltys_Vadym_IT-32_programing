"""Завдання 2. isinstance(), issubclass() та порядок пошуку методів."""
from task1 import LEADER_NAME, LEADER_PHONE, LEADER_SURNAME, GroupLeader, Person, Student

CLASSES = [Person, Student, GroupLeader]


def print_table(title, rows, check):
    """Друкує таблицю: рядки - об'єкти або класи, стовпці - класи ієрархії."""
    header = f"{title:<22}" + "".join(f"{cls.__name__:<13}" for cls in CLASSES)
    print(header.rstrip())
    print("-" * len(header.rstrip()))
    for label, item in rows:
        line = f"{label:<22}" + "".join(f"{str(check(item, cls)):<13}" for cls in CLASSES)
        print(line.rstrip())
    print()


def main():
    objects = [
        ("person (Person)", Person("Vadym", "Soltys")),
        ("me (Student)", Student("Vadym", "Soltys", "IT-32")),
        ("leader (GroupLeader)",
         GroupLeader(LEADER_NAME, LEADER_SURNAME, "IT-32", LEADER_PHONE)),
    ]
    print_table("isinstance(obj, cls)", objects, isinstance)
    print_table("issubclass(sub, cls)", [(cls.__name__, cls) for cls in CLASSES], issubclass)

    print("GroupLeader.__mro__:")
    for number, cls in enumerate(GroupLeader.__mro__, 1):
        own = "has own describe()" if "describe" in cls.__dict__ else "no describe()"
        print(f"  {number}. {cls.__name__:<12} {own}")


if __name__ == "__main__":
    main()
