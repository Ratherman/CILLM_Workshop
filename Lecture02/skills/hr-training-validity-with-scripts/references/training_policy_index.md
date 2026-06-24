# Training Policy Index

Use this index to route aviation workplace training validity questions. This is a demo reference, not an official company policy.

| Query Type | User Keywords | Reference / Script | Notes |
|---|---|---|---|
| Training validity calculation | 有效嗎、到期日、效期、剩幾天、需要複訓、是否過期 | `scripts/lookup_training_validity.py` | Use the script whenever a date calculation is required. |
| Dangerous goods training | 危險物品、dangerous goods、DG | `scripts/lookup_training_validity.py` | Map to `dangerous_goods`. |
| Aviation security training | 航空保安、保安訓練、security | `scripts/lookup_training_validity.py` | Map to `aviation_security`. |
| Safety management training | 安全管理、SMS、safety management | `scripts/lookup_training_validity.py` | Map to `safety_management_system`. |
| Ground service training | 地勤服務、旅客服務、ground service | `scripts/lookup_training_validity.py` | Map to `ground_service`. |
| Ramp safety training | 機坪安全、ramp safety、apron | `scripts/lookup_training_validity.py` | Map to `ramp_safety`. |
| Maintenance human factors | 修護人因、人因訓練、maintenance human factors | `scripts/lookup_training_validity.py` | Map to `maintenance_human_factors`. |
| Cabin safety recurrent | 空服安全複訓、客艙安全、cabin safety | `scripts/lookup_training_validity.py` | Map to `cabin_safety_recurrent`. |

## Required Script Arguments

- `training_type`: one of the supported English training IDs from `training_type_table.json`, such as `dangerous_goods`. Do not pass the Chinese display name as the script argument.
- `completion_date`: completion date in `YYYY-MM-DD`, `YYYY/MM/DD`, or similar date format.
- `as_of_date`: optional check date. If missing, pass null.

## Routing Rules

- If the user asks a general rule without a date, read `training_validity_rules.md` and explain what information is needed.
- If the user provides both training type and completion date, run `training_validity_lookup`.
- If training type is ambiguous, ask one clarifying question.
- If completion date is missing, ask for the completion date.
