"""Модуль для роботи з файлами: перегляд директорії, пошук і створення файлів."""

import os


def list_files(directory):
    """Повертає список файлів у директорії.

    Параметри:
        directory (str): шлях до директорії.

    Повертає:
        list[str]: відсортований список імен файлів (без піддиректорій).
    """
    return sorted(
        name for name in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, name))
    )


def find_files(directory, substring):
    """Шукає в директорії файли, у назві яких є підрядок (без урахування регістру).

    Параметри:
        directory (str): шлях до директорії.
        substring (str): підрядок, який шукаємо в назві файлу.

    Повертає:
        list[str]: список імен знайдених файлів (порожній, якщо нічого не знайдено).
    """
    substring = substring.lower()
    return [name for name in list_files(directory) if substring in name.lower()]


def create_file(path, text):
    """Створює новий файл із переданим текстом (кодування UTF-8).

    Параметри:
        path (str): шлях до файлу, який потрібно створити.
        text (str): текст, який буде записано у файл.

    Повертає:
        str: шлях до створеного файлу.
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
    return path


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        create_file(os.path.join(tmp, "report.txt"), "тест")
        create_file(os.path.join(tmp, "notes.txt"), "нотатки")
        create_file(os.path.join(tmp, "photo.png"), "...")
        os.mkdir(os.path.join(tmp, "subdir"))

        print("list_files:", list_files(tmp))
        print("find_files 'txt':", find_files(tmp, "txt"))
        print("find_files 'xyz':", find_files(tmp, "xyz"))

        assert list_files(tmp) == ["notes.txt", "photo.png", "report.txt"]
        assert find_files(tmp, "REPORT") == ["report.txt"]
        assert find_files(tmp, "xyz") == []
        print("Самоперевірка пройдена: усі assert виконано успішно.")
