from datetime import date


class Student:
    college = "FKTBP VNU"
    count = 0

    def __init__(self, name, surname, group, birth_year):
        self.name = name
        self.surname = surname
        self.group = group
        self.birth_year = birth_year
        Student.count += 1

    def full_name(self):
        return f"{self.name} {self.surname}"

    def age(self, year):
        return year - self.birth_year

    def card(self, year=None):
        if year is None:
            year = date.today().year
        lines = [
            self.full_name(),
            f"group: {self.group}",
            f"age in {year}: {self.age(year)}",
        ]
        width = max(len(line) for line in lines)
        border = "+" + "-" * (width + 2) + "+"
        body = [f"| {line:<{width}} |" for line in lines]
        return "\n".join([border, *body, border])


def main():
    me = Student("Vadym", "Soltys", "IT-32", 2009)
    other = Student("Vlad", "Kudrik", "IT-32", 2009)
    print(me.card(2026))
    print(other.card(2026))


if __name__ == "__main__":
    main()
