from pathlib import Path

import pytest

from expenses import load_expenses, parse_line, total_by_category

REAL_FILE = Path(__file__).resolve().parent / "data" / "expenses.csv"


# ---------- Завдання 2: assert ----------
def test_parse_line_valid():
    record = parse_line("2026-11-02;food;85.50;lunch")
    assert record["category"] == "food"
    assert record["amount"] == 85.5


def test_parse_line_returns_full_record():
    record = parse_line("2026-11-02;transport;30.00;bus")
    assert record == {"date": "2026-11-02", "category": "transport",
                      "amount": 30.0, "comment": "bus"}


def test_parse_line_amount_is_float():
    record = parse_line("2026-11-06;clothes;899;jacket")
    assert isinstance(record["amount"], float)


def test_parse_line_strips_spaces():
    record = parse_line("  2026-11-03 ; study ; 65.00 ; printing \n")
    assert record["category"] == "study"
    assert record["comment"] == "printing"


# ---------- Завдання 3: винятки ----------
def test_parse_line_bad_amount():
    with pytest.raises(ValueError):
        parse_line("2026-11-02;food;abc;lunch")


def test_parse_line_too_few_fields():
    with pytest.raises(ValueError):
        parse_line("2026-11-02;food;85.50")


def test_parse_line_too_many_fields():
    with pytest.raises(ValueError):
        parse_line("2026-11-02;food;85.50;lunch;extra")


def test_parse_line_empty_line():
    with pytest.raises(ValueError):
        parse_line("")


# ---------- Завдання 4: параметризація (5 рядків з файлу витрат) ----------
@pytest.mark.parametrize(
    "line, category, amount",
    [
        ("2026-11-02;food;85.50;lunch", "food", 85.5),
        ("2026-11-03;study;65.00;printing", "study", 65.0),
        ("2026-11-04;entertainment;250.00;cinema", "entertainment", 250.0),
        ("2026-11-06;clothes;899.00;jacket", "clothes", 899.0),
        ("2026-11-08;food;140.00;cafe", "food", 140.0),
    ],
)
def test_parse_line_from_my_file(line, category, amount):
    record = parse_line(line)
    assert record["category"] == category
    assert record["amount"] == amount


# ---------- Завдання 5: tmp_path ----------
def test_total_by_category(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text(
        "# date;category;amount;comment\n"
        "2026-09-21;food;85.50;lunch\n"
        "\n"
        "2026-09-22;food;14.50;coffee\n",
        encoding="utf-8",
    )
    totals = total_by_category(load_expenses(path))
    assert totals == {"food": 100.0}


def test_load_expenses_skips_comments_and_blank_lines(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text("# header\n\n2026-09-21;food;10;a\n   \n# note\n2026-09-22;fun;5;b\n",
                    encoding="utf-8")
    records = load_expenses(path)
    assert [r["category"] for r in records] == ["food", "fun"]


def test_total_rounds_to_two_digits():
    records = [{"category": "x", "amount": 0.1}, {"category": "x", "amount": 0.2}]
    assert total_by_category(records) == {"x": 0.3}


def test_total_by_category_real_file():
    totals = total_by_category(load_expenses(REAL_FILE))
    assert totals == {
        "food": 751.10,
        "transport": 75.00,
        "study": 65.00,
        "entertainment": 250.00,
        "clothes": 899.00,
    }
