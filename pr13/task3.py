import math
import sys
from datetime import datetime
from pathlib import Path

NAME = "Vadym Soltys"
GROUP = "IT-32"
UNITS = ["B", "KB", "MB", "GB"]
USAGE = "usage: python3 task3.py [--dry-run] <dir>"


def format_size(size):
    """Розмір у зручному вигляді; одиниця визначається через math.log."""
    if size < 1024:
        return f"{size} B"
    index = min(int(math.log(size, 1024)), len(UNITS) - 1)
    return f"{size / 1024 ** index:.1f} {UNITS[index]}"


def fail(message, code):
    print(message, file=sys.stderr)
    sys.exit(code)


def main():
    print(f"{NAME}, {GROUP}")

    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    rest = [a for a in args if a != "--dry-run"]
    if len(rest) != 1 or rest[0].startswith("--"):
        fail(USAGE, 2)

    root = Path(rest[0])
    if not root.is_dir():
        fail(f"error: {root} is not a directory", 1)

    # Збираємо файли (лише верхній рівень) разом з датою зміни
    entries = []
    for path in root.iterdir():
        if path.is_file():
            stat = path.stat()
            entries.append((path, stat.st_size, datetime.fromtimestamp(stat.st_mtime)))

    if not entries:
        print("no files to organize")
        return

    entries.sort(key=lambda e: e[2])  # від найстарішого до найновішого

    # План: (джерело, призначення)
    plan = []
    lines = []
    name_width = max(len(p.name) for p, _, _ in entries)
    size_width = max(len(format_size(s)) for _, s, _ in entries)
    for path, size, mtime in entries:
        folder = mtime.strftime("%Y-%m")
        plan.append((path, root / folder / path.name))
        lines.append(
            f"{path.name:<{name_width}}  {format_size(size):>{size_width}}  "
            f"{mtime.strftime('%d.%m.%Y %H:%M')}  -> {folder}/"
        )
    for line in lines:
        print(line)

    folders = {dst.parent for _, dst in plan}
    summary = f"{len(plan)} files, {len(folders)} folders"

    if dry_run:
        print(f"{summary} (dry run, nothing moved)")
        return

    # Спершу перевіряємо ВСІ конфлікти, і лише потім переміщуємо
    for _, dst in plan:
        if dst.exists():
            fail(f"error: {dst} already exists, nothing was moved", 1)

    run_time = datetime.now()
    for src, dst in plan:
        dst.parent.mkdir(exist_ok=True)
        src.rename(dst)
    print(summary)

    # Звіт поруч зі скриптом
    reports_dir = Path(__file__).resolve().parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    report_path = reports_dir / f"organize_{run_time.strftime('%Y%m%d_%H%M')}.txt"
    content = [
        f"{NAME}, {GROUP}",
        f"run: {run_time.strftime('%d.%m.%Y %H:%M')}",
        f"directory: {root}",
        *lines,
        summary,
    ]
    report_path.write_text("\n".join(content) + "\n", encoding="utf-8")
    print(f"report saved to: reports/{report_path.name}")


if __name__ == "__main__":
    main()
