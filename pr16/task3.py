import json
import sys
from pathlib import Path

NAME = "Vadym Soltys"
GROUP = "IT-32"
BASE = Path(__file__).resolve().parent
SETTINGS = BASE / "settings.json"
EXPENSES = BASE / "data" / "expenses.json"

DEFAULTS = {
    "owner": NAME,
    "group": GROUP,
    "currency": "UAH",
    "monthly_limit": 6000,
    "categories": ["food", "transport", "study", "entertainment", "clothes"],
}


def main():
    print(f"{NAME}, {GROUP}")

    if not SETTINGS.exists():
        with SETTINGS.open("w", encoding="utf-8") as f:
            json.dump(DEFAULTS, f, indent=2, ensure_ascii=False)
        print("settings.json not found, default created")
        return

    try:
        with SETTINGS.open(encoding="utf-8") as f:
            settings = json.load(f)
    except json.JSONDecodeError as error:
        # пошкоджений файл НЕ перезаписуємо: користувач має виправити його сам
        print(f"error: settings.json is corrupted at line {error.lineno}, "
              f"column {error.colno}: {error.msg}", file=sys.stderr)
        sys.exit(1)

    try:
        limit = float(settings["monthly_limit"])
        currency = settings["currency"]
    except KeyError as error:
        print(f"error: settings.json has no key {error}", file=sys.stderr)
        sys.exit(1)

    try:
        with EXPENSES.open(encoding="utf-8") as f:
            spent = sum(record["amount"] for record in json.load(f))
    except FileNotFoundError:
        print(f"error: {EXPENSES} not found (run task1.py first)", file=sys.stderr)
        sys.exit(1)

    print(f"owner: {settings.get('owner')}, group: {settings.get('group')}")
    print(f"categories: {', '.join(settings.get('categories', []))}")
    print(f"limit: {limit:.2f} {currency}, spent: {spent:.2f} {currency}, "
          f"left: {limit - spent:.2f} {currency}")
    if spent > limit:
        print("warning: monthly limit exceeded")


if __name__ == "__main__":
    main()
