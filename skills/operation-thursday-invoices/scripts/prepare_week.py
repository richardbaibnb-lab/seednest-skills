"""Plan the Thursday invoice folders; create them only with --create."""

import argparse
import json
import os
from datetime import datetime, time, timedelta, timezone
from pathlib import Path


TZ = timezone(timedelta(hours=10))
MAILBOXES = {
    "clean@seednest.com.au": "clean",
    "service@seednest.com.au": "service",
    "accounts@seednest.com.au": "accountant",
    "insurance@seednest.com.au": "insurance",
    "richardbaicouncil@gmail.com": "council",
    "energy@seednest.com.au": "energyl",
    "energyseednest@163.com": "george x energy",
}


def downloads_path():
    if os.name == "nt":
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
            ) as key:
                value, _ = winreg.QueryValueEx(
                    key, "{374DE290-123F-4565-9164-39C4925E467B}"
                )
            path = Path(os.path.expandvars(value))
            if not path.is_absolute():
                raise ValueError("The configured Downloads path is not absolute")
            return path
        except FileNotFoundError:
            pass
    return Path.home() / "Downloads"


def week_window(now, week_ending=None):
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("The current time must include a UTC offset")
    now = now.astimezone(TZ)
    if week_ending:
        date = datetime.strptime(week_ending, "%Y-%m-%d").date()
        if date.weekday() != 3:
            raise ValueError("--week-ending must be a Thursday")
        end = datetime.combine(date, time(9), TZ)
        if end > now:
            raise ValueError("The selected weekly period has not ended yet")
    else:
        date = now.date() - timedelta(days=(now.weekday() - 3) % 7)
        end = datetime.combine(date, time(9), TZ)
        if end > now:
            end -= timedelta(days=7)
    return end - timedelta(days=7), end


def prepare(now, week_ending=None, downloads=None, create=False):
    start, end = week_window(now, week_ending)
    base = Path(downloads).expanduser() if downloads is not None else downloads_path()
    if not base.is_absolute():
        raise ValueError("Downloads must be an absolute path")
    root = base / "周度invoice更新" / f"{start:%Y.%m.%d} - {end:%Y.%m.%d}"
    folders = {mailbox: root / name for mailbox, name in MAILBOXES.items()}
    # Check every target before making changes. Existing content is never removed.
    for path in [root, *folders.values()]:
        if path.exists() and not path.is_dir():
            raise ValueError(f"A required directory path is occupied by a file: {path}")
    if create:
        for path in folders.values():
            path.mkdir(parents=True, exist_ok=True)
    return {
        "start_inclusive": start.isoformat(),
        "end_exclusive": end.isoformat(),
        "timezone": "UTC+10:00 (fixed)",
        "root": str(root),
        "folders": {mailbox: str(path) for mailbox, path in folders.items()},
        "directories_prepared": create,
        "mailbox_scan_performed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week-ending", help="An already reached Thursday, YYYY-MM-DD")
    parser.add_argument("--downloads", help="Absolute Downloads base directory")
    parser.add_argument("--create", action="store_true", help="Create missing directories")
    parser.add_argument("--now", help="Override current time with an offset-aware ISO timestamp")
    args = parser.parse_args()
    try:
        now = datetime.fromisoformat(args.now) if args.now else datetime.now(TZ)
        result = prepare(now, args.week_ending, args.downloads, args.create)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
