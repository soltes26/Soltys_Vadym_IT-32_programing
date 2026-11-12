import json
import re
from datetime import date

NAME = "Vadym Soltys"
GROUP = "IT-32"

ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def default_iso(obj):
    """Для параметра default=: викликається лише для типів, яких JSON не знає."""
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def encode_dates(obj):
    """Рекурсивно замінює date на рядок ISO."""
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {key: encode_dates(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [encode_dates(item) for item in obj]
    return obj


def decode_dates(obj):
    """Рекурсивно замінює рядки формату YYYY-MM-DD назад на date."""
    if isinstance(obj, str) and ISO_DATE.fullmatch(obj):
        try:
            return date.fromisoformat(obj)
        except ValueError:
            return obj
    if isinstance(obj, dict):
        return {key: decode_dates(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [decode_dates(item) for item in obj]
    return obj


def main():
    print(f"{NAME}, {GROUP}")
    data = {
        "owner": NAME,
        "created": date(2026, 11, 12),
        "expenses": [
            {"date": date(2026, 11, 2), "category": "food", "amount": 85.5},
            {"date": date(2026, 11, 3), "category": "study", "amount": 65.0},
        ],
    }

    print("--- plain json.dumps")
    try:
        json.dumps(data)
    except TypeError as error:
        print(f"TypeError: {error}")

    print("--- way 1: default=")
    text = json.dumps(data, default=default_iso, ensure_ascii=False)
    print(text)
    back = json.loads(text)
    print(f"type of created after loads: {type(back['created']).__name__}")
    print(f"back == data: {back == data}")

    print("--- way 2: encode_dates / decode_dates")
    text = json.dumps(encode_dates(data), ensure_ascii=False)
    print(text)
    back = decode_dates(json.loads(text))
    print(f"type of created after loads: {type(back['created']).__name__}")
    print(f"type of expenses[0]['date']: {type(back['expenses'][0]['date']).__name__}")
    print(f"back == data: {back == data}")


if __name__ == "__main__":
    main()
