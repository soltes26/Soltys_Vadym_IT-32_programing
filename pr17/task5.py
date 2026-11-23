import json
import sys
from datetime import datetime
from pathlib import Path

import requests

NAME = "Vadym Soltys"
GROUP = "IT-32"
URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
TIMEOUT = 10
CACHE = Path(__file__).resolve().parent / "cache" / "rates.json"
MAX_AGE = 3600  # 1 година, секунд


def load_cache():
    """Повертає (дані, вік у секундах) або None, якщо кешу немає, він застарів чи пошкоджений."""
    if not CACHE.is_file():
        return None
    try:
        with CACHE.open(encoding="utf-8") as f:
            cached = json.load(f)
        saved_at = datetime.fromisoformat(cached["saved_at"])
        data = cached["data"]
    except (json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"warning: cache is damaged, ignoring it ({error})", file=sys.stderr)
        return None
    age = (datetime.now() - saved_at).total_seconds()
    if age >= MAX_AGE:
        return None
    return data, age


def fetch_and_save():
    try:
        response = requests.get(URL, params={"json": ""}, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)

    CACHE.parent.mkdir(exist_ok=True)
    with CACHE.open("w", encoding="utf-8") as f:
        json.dump({"saved_at": datetime.now().isoformat(timespec="seconds"), "data": data},
                  f, indent=2, ensure_ascii=False)
    return data


def main():
    print(f"{NAME}, {GROUP}")
    cached = load_cache()
    if cached is not None:
        data, age = cached
        print(f"source: cache (age {age:.0f} s)")
    else:
        data = fetch_and_save()
        print("source: api (cache saved)")
    print(f"currencies: {len(data)}")


if __name__ == "__main__":
    main()
