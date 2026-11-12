"""Функції для роботи з файлом витрат (без print: лише повернення результату)."""

from pathlib import Path


def parse_line(line):
    """Розбирає рядок 'дата;категорія;сума;коментар' у словник.

    Генерує ValueError, якщо полів не чотири або сума не є числом.
    """
    parts = [part.strip() for part in line.strip().split(";")]
    if len(parts) != 4:
        raise ValueError(f"expected 4 fields, got {len(parts)}: {line!r}")
    date, category, amount_text, comment = parts
    try:
        amount = float(amount_text)
    except ValueError:
        raise ValueError(f"amount is not a number: {amount_text!r}") from None
    return {"date": date, "category": category, "amount": amount, "comment": comment}


def total_by_category(records):
    """Повертає {категорія: сума}, суми округлені до двох знаків."""
    totals = {}
    for record in records:
        category = record["category"]
        totals[category] = totals.get(category, 0.0) + record["amount"]
    return {category: round(total, 2) for category, total in totals.items()}


def load_expenses(path):
    """Читає файл витрат; коментарі (#) та порожні рядки пропускає."""
    records = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        records.append(parse_line(line))
    return records
