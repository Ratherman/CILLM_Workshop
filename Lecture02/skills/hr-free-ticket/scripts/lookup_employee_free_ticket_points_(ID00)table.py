# 依員工年資年數查詢 ID00 免費機票點數。
# - 固定讀取 references/employee_free_ticket_points_(ID00)table.json
# - 輸入年資年數，輸出 JSON 

from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

SOURCE_TABLE_FILENAME = "employee_free_ticket_points_(ID00)table.json"
SOURCE_TABLE_NAME = "員工優待機票免票 (ID00) 點數對照表"

def output(payload: dict[str, Any]) -> int: # 輸出 JSON
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def resolve_table_path() -> Path | None:
    # 固定讀取 references/employee_free_ticket_points_(ID00)table.json
    references_dir = Path(__file__).resolve().parent.parent / "references"
    path = references_dir / SOURCE_TABLE_FILENAME
    return path if path.exists() else None


def parse_seniority_years(raw_value: str | None) -> int | None:
    # 把輸入轉成正整數年資
    if raw_value is None or raw_value.strip() == "":
        return None

    value = raw_value.strip()
    if not value.isdigit():
        return None

    years = int(value)
    if years <= 0:
        return None
    
    return years


def load_table(table_path: Path) -> dict[str, Any]:
    # 讀取 JSON 對照表
    with table_path.open("r", encoding="utf-8") as file:
        table = json.load(file)
        return table


def available_years(rules: list[dict[str, Any]]) -> list[int]:
    # 整理目前表格中可查詢的年資年數, 用於查不到資料時回報
    years: list = []

    for rule in rules:
        year = rule.get("年資年數")

        if isinstance(year, int):
            years.append(year)

    result = sorted(years)

    return result


def lookup_points(seniority_years: int, table: dict[str, Any]) -> dict[str, Any] | None:
    # 依年資年數在 JSON table 中查出原優待機票點數與調整配點

    rules = table.get("rules", [])

    if not isinstance(rules, list):
        return None

    for rule in rules:
        if rule.get("年資年數") != seniority_years:
            continue
        points_rule = rule.get("點數規範", {})

        if not isinstance(points_rule, dict):
            return None
        
        original_points = points_rule.get("原優待機票點數")
        adjusted_points = points_rule.get("調整配點")

        points_results =  {
            "seniority_years": seniority_years,
            "original_points": original_points,
            "adjusted_points": adjusted_points,
        }

        return points_results
    return None


def build_parser() -> argparse.ArgumentParser:
    # create CLI parser
    parser = argparse.ArgumentParser(description="Lookup ID00 free-ticket points by seniority years.")
    parser.add_argument("seniority_years", nargs="?")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    raw_years = args.seniority_years
    seniority_years = parse_seniority_years(raw_years)

    if seniority_years is None:
        # 缺少年資或年資格式不正確
        seniority_years_none_report = output(
            {
                "status": False,
                "message": "請提供正整數年資年數",
                "seniority_years": raw_years,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": SOURCE_TABLE_FILENAME
            }
        )
        return seniority_years_none_report

    table_path = resolve_table_path()
    if table_path is None or not table_path.exists():
        # 找不到來源表時回報資料源缺失
        return output(
            {
                "status": False,
                "message": "找不到員工優待機票免票 (ID00) 點數對照表",
                "seniority_years": seniority_years,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": SOURCE_TABLE_FILENAME
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
                "seniority_years": seniority_years,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": table_path.name
            }
        )

    rules = table.get("rules", [])
    if not isinstance(rules, list):
        # schema 檢查, 要求表格必須有 rules list
        return output(
            {
                "status": False,
                "message": "員工優待機票免票 (ID00) 點數對照表缺少完整規範 list",
                "seniority_years": seniority_years,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": table_path.name
            }
        )

    result = lookup_points(seniority_years, table)
    if result is None:
        # 年資不在表內時, 回傳目前可查年資
        return output(
            {
                "status": False,
                "message": f"資料未列出 {seniority_years} 年資年數，請洽人力資源部門",
                "seniority_years": seniority_years,
                "source_name": SOURCE_TABLE_NAME,
                "source_file": table_path.name
            }
        )

    final_report =  output(
        {
            "status": True,
            "seniority_years": result["seniority_years"],
            "original_points": result["original_points"],
            "adjusted_points": result["adjusted_points"],
            "source_name": SOURCE_TABLE_NAME,
            "source_file": SOURCE_TABLE_FILENAME
        }
    )

    return final_report


if __name__ == "__main__":
    raise SystemExit(main())
