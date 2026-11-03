"""Програма, що використовує модуль soltys_files."""

import os

import soltys_files

DIRECTORY = os.path.expanduser("~/Documents")
if not os.path.isdir(DIRECTORY):
    DIRECTORY = os.path.expanduser("~")

files = soltys_files.list_files(DIRECTORY)
print(f"Файли в каталозі {DIRECTORY}:")
for name in files:
    print("  ", name)

substring = "txt"
found = soltys_files.find_files(DIRECTORY, substring)
print(f"\nФайли, що містять '{substring}': {found}")

info_path = os.path.join(DIRECTORY, "student_info.txt")
text = "Ім'я: Вадим\nПрізвище: Солтис\nГрупа: IT-32\n"
created = soltys_files.create_file(info_path, text)
print(f"\nСтворено файл: {created}")
print("Вміст:")
print(open(created, encoding="utf-8").read())
