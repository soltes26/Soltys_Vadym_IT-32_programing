import math
import sys
from pathlib import Path

import requests

NAME = "Vadym Soltys"
GROUP = "IT-32"
URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
TIMEOUT = 10
EXPENSES = Path(__file__).resolve().parent / "data" / "expenses.csv"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def read_total(path):
    """Сума витрат у гривнях (math.fsum); коментарі та порожні рядки пропускаються."""
    amounts = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(";")
        try:
            amounts.append(float(parts[2]))
        except (IndexError, ValueError):
            print(f"warning: line {number} skipped: {line}", file=sys.stderr)
    return math.fsum(amounts)


def get_rate(code):
    """Курс однієї валюти окремим запитом з параметром valcode."""
    try:
        response = requests.get(URL, params={"valcode": code, "json": ""}, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except requests.Timeout:
        # Timeout перевіряємо ПЕРЕД ConnectionError: ConnectTimeout належить до обох
        fail(f"request for {code} timed out after {TIMEOUT} s")
    except requests.ConnectionError:
        fail("no connection to the server (check your internet)")
    except requests.HTTPError as error:
        fail(f"server returned an error: {error.response.status_code} {error.response.reason}")
    except requests.RequestException as error:
        fail(f"request failed: {error}")

    if not data:
        fail(f"no rate for {code} in the response")
    return data[0]["rate"], data[0]["exchangedate"]


def main():
    print(f"{NAME}, {GROUP}")
    if not EXPENSES.is_file():
        fail(f"{EXPENSES} not found")

    total = read_total(EXPENSES)
    usd_rate, rate_date = get_rate("USD")
    eur_rate, _ = get_rate("EUR")

    print(f"rate date: {rate_date}")
    print(f"total: {total:.2f} UAH = {total / usd_rate:.2f} USD = {total / eur_rate:.2f} EUR")


if __name__ == "__main__":
    main()
