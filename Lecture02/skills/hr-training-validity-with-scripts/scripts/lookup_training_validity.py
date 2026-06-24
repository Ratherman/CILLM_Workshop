from __future__ import annotations

import calendar
import json
import sys
from datetime import date, datetime
from pathlib import Path


TABLE_PATH = Path(__file__).resolve().parent.parent / "references" / "training_type_table.json"


def parse_date(value: str | None) -> date | None:
    if value is None or not str(value).strip():
        return None

    raw = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y%m%d"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Unsupported date format: {value}")


def add_months(day: date, months: int) -> date:
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day.day, last_day))


def load_table() -> list[dict]:
    return json.loads(TABLE_PATH.read_text(encoding="utf-8"))


def normalize(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def find_training(training_type: str, table: list[dict]) -> dict | None:
    target = normalize(training_type)
    for row in table:
        candidates = [row["training_type"], row["display_name_zh"], *row.get("keywords", [])]
        if any(target == normalize(str(candidate)) for candidate in candidates):
            return row
    for row in table:
        candidates = [row["display_name_zh"], *row.get("keywords", [])]
        if any(str(candidate).lower() in training_type.lower() for candidate in candidates):
            return row
    return None


def main(argv: list[str]) -> int:
    training_type = argv[1] if len(argv) > 1 else ""
    completion_date_raw = argv[2] if len(argv) > 2 else ""
    as_of_date_raw = argv[3] if len(argv) > 3 else ""

    if not training_type.strip():
        raise ValueError("training_type is required")
    if not completion_date_raw.strip():
        raise ValueError("completion_date is required")

    table = load_table()
    training = find_training(training_type, table)
    if training is None:
        known = [row["training_type"] for row in table]
        result = {
            "matched": False,
            "input_training_type": training_type,
            "known_training_types": known,
            "error": "unknown_training_type",
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0

    completion_date = parse_date(completion_date_raw)
    as_of_date = parse_date(as_of_date_raw) or date.today()
    valid_until = add_months(completion_date, int(training["valid_months"]))
    days_remaining = (valid_until - as_of_date).days

    if days_remaining < 0:
        status = "expired"
        recommendation = "training_expired_arrange_retraining"
    elif days_remaining <= int(training["renewal_notice_days"]):
        status = "renewal_due_soon"
        recommendation = "arrange_recurrent_training"
    else:
        status = "valid"
        recommendation = "no_immediate_retraining_needed"

    result = {
        "matched": True,
        "training_type": training["training_type"],
        "display_name_zh": training["display_name_zh"],
        "completion_date": completion_date.isoformat(),
        "as_of_date": as_of_date.isoformat(),
        "valid_months": training["valid_months"],
        "renewal_notice_days": training["renewal_notice_days"],
        "valid_until": valid_until.isoformat(),
        "days_remaining": days_remaining,
        "status": status,
        "recommendation": recommendation,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
