# 依身分、折扣別、艙等、員工狀態與年資月數查詢優待機票額度。
# - 固定讀取 references/preferential_ticket_rules_summary_table.json
# - 輸入查詢條件，輸出 JSON

from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

SOURCE_TABLE_FILENAME = "preferential_ticket_rules_summary_table.json"
SOURCE_TABLE_NAME = "優待機票規定概要表"
RETIRED_EMPLOYEE_STATUS = "國內退休(職)員工"


def output(payload: dict[str, Any]) -> int:  # 輸出 JSON
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def resolve_table_path() -> Path | None:
    # 固定讀取 references/preferential_ticket_rules_summary_table.json
    references_dir = Path(__file__).resolve().parent.parent / "references"
    path = references_dir / SOURCE_TABLE_FILENAME
    return path if path.exists() else None


def normalize_text(raw_value: str | None) -> str | None:
    # 將文字輸入去除前後空白；空字串視為未提供
    if raw_value is None:
        return None

    value = raw_value.strip()
    if value == "":
        return None

    return value


def parse_seniority_months(raw_value: str | None, employee_status: str | None) -> int | None:
    # 現職員工需要年資月數；國內退休(職)員工在表格中為不適用
    if employee_status == RETIRED_EMPLOYEE_STATUS:
        return None

    if raw_value is None or raw_value.strip() == "":
        return None

    value = raw_value.strip()
    if not value.isdigit():
        return None

    months = int(value)
    if months < 0:
        return None

    return months


def load_table(table_path: Path) -> dict[str, Any]:
    # 讀取 JSON 對照表
    with table_path.open("r", encoding="utf-8") as file:
        table = json.load(file)
        return table


def rule_matches(
    rule: dict[str, Any],
    identity_group: str,
    discount_type: str,
    cabin: str,
) -> bool:
    # 比對外層規則：身分、折扣別與艙等必須完全相同
    return (
        rule.get("身分") == identity_group
        and rule.get("折扣別") == discount_type
        and rule.get("艙等") == cabin
    )


def status_rule_matches(
    status_rule: dict[str, Any],
    employee_status: str,
    seniority_months: int | None,
) -> bool:
    # 比對員工狀態；退休(職)員工的年資月數在表格中為不適用
    if status_rule.get("員工狀態") != employee_status:
        return False

    lower_bound = status_rule.get("年資月數下限")
    upper_bound = status_rule.get("年資月數上限")

    if lower_bound == "不適用" and upper_bound == "不適用":
        return True

    if not isinstance(lower_bound, int):
        return False

    if seniority_months is None or seniority_months < lower_bound:
        return False

    if isinstance(upper_bound, int) and seniority_months > upper_bound:
        return False

    return True


def lookup_quota(
    identity_group: str,
    discount_type: str,
    cabin: str,
    employee_status: str,
    seniority_months: int | None,
    table: dict[str, Any],
) -> dict[str, Any] | None:
    # 依查詢條件在 JSON table 中查出額度
    rules = table.get("rules", [])

    if not isinstance(rules, list):
        return None

    for rule in rules:
        if not isinstance(rule, dict):
            continue

        if not rule_matches(rule, identity_group, discount_type, cabin):
            continue

        status_rules = rule.get("員工狀態規則", [])
        if not isinstance(status_rules, list):
            return None

        for status_rule in status_rules:
            if not isinstance(status_rule, dict):
                continue

            if not status_rule_matches(status_rule, employee_status, seniority_months):
                continue

            quota_result = {
                "identity_group": identity_group,
                "discount_type": discount_type,
                "cabin": cabin,
                "employee_status": employee_status,
                "seniority_months": seniority_months,
                "quota": status_rule.get("額度"),
            }

            return quota_result

    return None


def build_parser() -> argparse.ArgumentParser:
    # create CLI parser
    parser = argparse.ArgumentParser(description="Lookup preferential ticket quota from summary table.")
    parser.add_argument("identity_group", nargs="?")
    parser.add_argument("discount_type", nargs="?")
    parser.add_argument("cabin", nargs="?")
    parser.add_argument("employee_status", nargs="?")
    parser.add_argument("seniority_months", nargs="?")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    identity_group = normalize_text(args.identity_group)
    discount_type = normalize_text(args.discount_type)
    cabin = normalize_text(args.cabin)
    employee_status = normalize_text(args.employee_status)
    seniority_months = parse_seniority_months(args.seniority_months, employee_status)

    if not identity_group or not discount_type or not cabin or not employee_status:
        # 缺少基本查詢條件
        return output(
            {
                "status": False,
                "message": "請提供身分、折扣別、艙等與員工狀態",
                "identity_group": identity_group,
                "discount_type": discount_type,
                "cabin": cabin,
                "employee_status": employee_status,
                "seniority_months": args.seniority_months,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": SOURCE_TABLE_FILENAME,
            }
        )

    if employee_status != RETIRED_EMPLOYEE_STATUS and seniority_months is None:
        # 現職員工需要正確的年資月數才能查詢額度
        return output(
            {
                "status": False,
                "message": "請提供非負整數年資月數",
                "identity_group": identity_group,
                "discount_type": discount_type,
                "cabin": cabin,
                "employee_status": employee_status,
                "seniority_months": args.seniority_months,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": SOURCE_TABLE_FILENAME,
            }
        )

    table_path = resolve_table_path()
    if table_path is None or not table_path.exists():
        # 找不到來源表時回報資料源缺失
        return output(
            {
                "status": False,
                "message": "找不到優待機票規定概要表",
                "identity_group": identity_group,
                "discount_type": discount_type,
                "cabin": cabin,
                "employee_status": employee_status,
                "seniority_months": seniority_months,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": SOURCE_TABLE_FILENAME,
            }
        )

    try:
        table = load_table(table_path)

    except json.JSONDecodeError as e:
        # JSON 格式壞掉時, 回報檔名與 parser 錯誤
        return output(
            {
                "status": False,
                "message": f"table invalid error: {e}",
                "identity_group": identity_group,
                "discount_type": discount_type,
                "cabin": cabin,
                "employee_status": employee_status,
                "seniority_months": seniority_months,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": table_path.name,
            }
        )

    rules = table.get("rules", [])
    if not isinstance(rules, list):
        # schema 檢查, 要求表格必須有 rules list
        return output(
            {
                "status": False,
                "message": "優待機票規定概要表缺少完整規範 list",
                "identity_group": identity_group,
                "discount_type": discount_type,
                "cabin": cabin,
                "employee_status": employee_status,
                "seniority_months": seniority_months,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": table_path.name,
            }
        )

    result = lookup_quota(identity_group, discount_type, cabin, employee_status, seniority_months, table)
    if result is None:
        # 查不到完全符合條件的規則時, 不自行推測近似額度
        return output(
            {
                "status": False,
                "message": "資料未列出符合條件的優待機票額度，請確認查詢條件或洽人力資源部門",
                "identity_group": identity_group,
                "discount_type": discount_type,
                "cabin": cabin,
                "employee_status": employee_status,
                "seniority_months": seniority_months,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": table_path.name,
            }
        )

    final_report = output(
        {
            "status": True,
            "identity_group": result["identity_group"],
            "discount_type": result["discount_type"],
            "cabin": result["cabin"],
            "employee_status": result["employee_status"],
            "seniority_months": result["seniority_months"],
            "quota": result["quota"],
            "source_name": SOURCE_TABLE_NAME,
            "source_file": SOURCE_TABLE_FILENAME,
        }
    )

    return final_report


if __name__ == "__main__":
    raise SystemExit(main())
