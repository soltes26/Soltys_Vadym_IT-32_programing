from task1 import Student


def main():
    me = Student("Vadym", "Soltys", "IT-32", 2009)
    other = Student("Vlad", "Kudrik", "IT-32", 2009)

    print("--- атрибут класу college")
    print("Student.college:", Student.college)
    print("me.college:     ", me.college)
    print("other.college:  ", other.college)

    print("--- присвоєння через об'єкт: me.college = 'Another college'")
    me.college = "Another college"
    print("Student.college:", Student.college)
    print("me.college:     ", me.college)
    print("other.college:  ", other.college)

    print("--- де що зберігається")
    print("me.__dict__:   ", me.__dict__)
    print("other.__dict__:", other.__dict__)
    class_attrs = {k: v for k, v in Student.__dict__.items()
                   if not k.startswith("__") and not callable(v)}
    print("Student.__dict__ (без методів і службових):", class_attrs)
    print("методи в Student.__dict__:",
          [k for k, v in Student.__dict__.items() if callable(v) and not k.startswith("__")])

    print("--- лічильник")
    print("Student.count:", Student.count)


if __name__ == "__main__":
    main()
