import sys

import requests

NAME = "Vadym Soltys"
GROUP = "IT-32"
URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
TIMEOUT = 10


def find_rate(rates, code):
    for item in rates:
        if item["cc"] == code:
            return item
    return None


def main():
    print(f"{NAME}, {GROUP}")
    try:
        response = requests.get(URL, params={"json": ""}, timeout=TIMEOUT)
        response.raise_for_status()
        rates = response.json()
    except requests.RequestException as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)

    print("status:", response.status_code)
    print("content-type:", response.headers.get("Content-Type"))
    print("currencies:", len(rates))
    for code in ("USD", "EUR"):
        item = find_rate(rates, code)
        if item is None:
            print(f"{code}: not found in response", file=sys.stderr)
            sys.exit(1)
        print(f"{code}: {item['rate']} UAH ({item['txt']}), date {item['exchangedate']}")


if __name__ == "__main__":
    main()
