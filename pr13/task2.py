import math
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

NAME = "Vadym Soltys"
GROUP = "IT-32"
EXPENSES = Path(__file__).resolve().parent / "data" / "expenses.csv"


def read_expenses(path):
    """Повертає словник {дата: сума за день}."""
    totals = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(";")
        try:
            if len(parts) < 3:
                raise ValueError("too few fields")
            day = datetime.strptime(parts[0].strip(), "%Y-%m-%d").date()
            amount = float(parts[2])
        except ValueError as error:
            print(f"warning: line {number} skipped ({error}): {line}", file=sys.stderr)
            continue
        totals[day] = totals.get(day, 0.0) + amount
    return totals


def first_of_next_month(day):
    return (day.replace(day=1) + timedelta(days=32)).replace(day=1)


def days_in_month(day):
    first = day.replace(day=1)
    return (first_of_next_month(day) - first).days


def main():
    print(f"{NAME}, {GROUP}")

    if "--check" in sys.argv[1:]:
        for d in (date(2026, 12, 15), date(2028, 2, 10)):
            print(f"{d}: {days_in_month(d)} days")
        return

    if not EXPENSES.is_file():
        print(f"error: {EXPENSES} not found", file=sys.stderr)
        sys.exit(1)
    totals = read_expenses(EXPENSES)
    if not totals:
        print("error: no valid expenses", file=sys.stderr)
        sys.exit(1)

    first, last = min(totals), max(totals)
    period = (last - first).days + 1
    print(f"period: {first:%d.%m.%Y} ({first:%A}) - {last:%d.%m.%Y} ({last:%A}), {period} days")
    print()

    # усі дні періоду, дні без витрат = 0
    days = [first + timedelta(days=i) for i in range(period)]
    daily = [totals.get(d, 0.0) for d in days]

    by_weekday = [0.0] * 7
    for d, amount in zip(days, daily):
        by_weekday[d.weekday()] += amount
    monday = date(2026, 1, 5)  # будь-який понеділок, лише для назв
    print("weekday      total")
    for i in range(7):
        name = (monday + timedelta(days=i)).strftime("%A")
        print(f"{name:<10} {by_weekday[i]:8.2f}")
    print()

    total = math.fsum(daily)
    mean = total / period
    std = math.sqrt(math.fsum((x - mean) ** 2 for x in daily) / period)
    print(f"total:        {total:.2f}")
    print(f"per day:      {mean:.2f} +- {std:.2f}")

    top_day = max(totals, key=totals.get)
    print(f"top day:      {top_day:%d.%m.%Y} ({top_day:%A}), {totals[top_day]:.2f}")
    print(f"no-spend days: {daily.count(0.0)}")

    month_days = days_in_month(last)
    left = (first_of_next_month(last) - last).days - 1
    print(f"days in {last:%B}: {month_days}, left after {last:%d.%m}: {left}")
    print(f"month forecast: {mean * month_days:.2f}")


if __name__ == "__main__":
    main()
