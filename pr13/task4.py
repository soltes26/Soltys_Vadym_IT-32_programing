import math
import random
import sys
from datetime import datetime
from pathlib import Path

NAME = "Vadym Soltys"
GROUP = "IT-32"
YEAR = 2009  # рік народження

HISTORY = Path(__file__).resolve().parent / "results" / "history.csv"
HEADER = "# datetime;score;seconds"
DATE_FORMAT = "%Y-%m-%d %H:%M"


def make_questions():
    """5 прикладів: числа з random, відповіді з math."""
    random.seed(YEAR)
    questions = []

    root = random.randint(5, 20)
    n = root * root
    questions.append((f"sqrt({n})", math.isqrt(n)))

    n = random.randint(4, 8)
    questions.append((f"{n}!", math.factorial(n)))

    g = random.randint(2, 9)
    a = g * random.randint(2, 9)
    b = g * random.randint(2, 9)
    questions.append((f"gcd({a}, {b})", math.gcd(a, b)))

    n = random.randint(5, 9)
    k = random.randint(2, 4)
    questions.append((f"comb({n}, {k})", math.comb(n, k)))

    percent = random.choice([5, 10, 15, 20, 25])
    value = random.randint(10, 50) * 20  # кратне 20, щоб відповідь була цілою
    questions.append((f"{percent}% of {value}", percent * value // 100))

    return questions


def read_history():
    attempts = []
    if not HISTORY.exists():
        return attempts
    for number, line in enumerate(HISTORY.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            stamp, score, seconds = line.split(";")
            attempts.append((stamp, int(score), float(seconds)))
        except ValueError:
            print(f"warning: line {number} skipped: {line!r}", file=sys.stderr)
    return attempts


def append_history(stamp, score, seconds):
    HISTORY.parent.mkdir(exist_ok=True)
    is_new = not HISTORY.exists()
    with HISTORY.open("a", encoding="utf-8") as f:
        if is_new:
            f.write(HEADER + "\n")
        f.write(f"{stamp};{score};{seconds:.1f}\n")


def main():
    print(f"{NAME}, {GROUP}")
    questions = make_questions()
    score = 0

    start = datetime.now()
    for number, (text, answer) in enumerate(questions, 1):
        try:
            raw = input(f"{number}) {text} = ")
        except EOFError:
            raw = ""
        try:
            given = int(raw.strip())
        except ValueError:
            given = None  # нечислова відповідь — неправильна

        if given == answer:
            score += 1
            print("   correct")
        else:
            print(f"   wrong, answer: {answer}")
    finish = datetime.now()

    seconds = round((finish - start).total_seconds(), 1)
    print(f"score: {score}/{len(questions)}, time: {seconds:.1f} s")

    try:
        append_history(finish.strftime(DATE_FORMAT), score, seconds)
    except OSError as error:
        print(f"error: cannot write history: {error}", file=sys.stderr)
        sys.exit(1)

    attempts = read_history()
    best = max(attempts, key=lambda a: (a[1], -a[2]))  # більше балів, менше часу
    print(
        f"attempts: {len(attempts)}, best: {best[1]}/{len(questions)} "
        f"in {best[2]:.1f} s ({best[0]})"
    )


if __name__ == "__main__":
    main()
