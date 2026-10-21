"""Read-only scheduling gate for Seednest's Melbourne 09:00 publishing queue."""
import argparse
import json
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("Australia/Melbourne")
PILLARS = ("regional", "owner_questions", "regional", "design_setup", "regional", "owner_questions", "design_setup")

def instant(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamp must include a UTC offset")
    return parsed

def inspect(state, now, force=False):
    local = now.astimezone(ZONE)
    target = datetime.combine(local.date(), time(9), ZONE)
    if target <= local:
        target += timedelta(days=1)
    next_check = state.get("next_check_at")
    due = force or not next_check or now >= instant(next_check)
    return {
        "business_work_due": due,
        "local_now": local.isoformat(),
        "target_date": target.date().isoformat(),
        "target_local": target.isoformat(),
        "target_utc": target.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "pillar": PILLARS[target.weekday()],
        "next_check_at": next_check,
        "reason": "review_previous_publication_and_prepare_next_slot" if due else "already_queued_wait_for_review"
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True)
    parser.add_argument("--now", help="Offset-aware ISO time for deterministic checks")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    path = Path(args.state)
    state = json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}
    now = instant(args.now) if args.now else datetime.now(timezone.utc)
    print(json.dumps(inspect(state, now, args.force), ensure_ascii=False))

if __name__ == "__main__":
    main()

