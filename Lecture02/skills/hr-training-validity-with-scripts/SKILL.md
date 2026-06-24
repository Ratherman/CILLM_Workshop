---
name: hr-training-validity-with-scripts
description: Helps employees check whether aviation workplace training or certificate records are still valid using a deterministic lookup script. Use when the user asks about training completion dates, recurrent training, certificate validity, expiration dates, remaining days, renewal timing, or whether retraining should be arranged. This demo skill covers dangerous goods, aviation security, safety management, ground service, ramp safety, maintenance human factors, and cabin safety recurrent training.

capabilities:
  - training_validity_check
  - certificate_expiration_query
  - recurrent_training_due_query

response_language: zh-TW

references:
  training_policy_index:
    path: ./references/training_policy_index.md
    description: Routing index used to select training validity rules and the lookup script.

  training_validity_rules:
    path: ./references/training_validity_rules.md
    description: General rules for interpreting training completion dates, validity months, expiration dates, and renewal status.

scripts:
  training_validity_lookup:
    path: ./scripts/lookup_training_validity.py
    description: Calculate training expiration date, status, days remaining, and renewal recommendation from training type, completion date, and optional as-of date.
---

# HR Training Validity Skill

This demo skill answers training or certificate validity questions for aviation workplace scenarios.

Use Traditional Chinese by default. Do not claim these are official company rules. Use the script for date calculation instead of calculating dates manually.

## Main Workflow

1. Read `training_policy_index` to identify the relevant reference and script.
2. If the user asks whether training is still valid, when it expires, or whether retraining is needed, use `training_validity_lookup`.
3. Provide `training_type`, `completion_date`, and optional `as_of_date` to the script.
   - `training_type` must be the English ID from `training_type_table.json`, such as `dangerous_goods`, not the Chinese display name.
4. If `as_of_date` is missing, pass null and let the script use today's date.
5. If the user does not provide a completion date, ask for it.
6. If the training type is unclear, ask the user to choose or describe the training.

## Supported Training Examples

- 危險物品訓練
- 航空保安訓練
- 安全管理系統訓練
- 地勤服務訓練
- 機坪安全訓練
- 修護人因訓練
- 空服安全複訓

## Response Rules

- Always base validity dates and remaining days on script results.
- Explain the result in plain Traditional Chinese.
- If the script returns `expired`, clearly say the training has expired as of the as-of date.
- If the script returns `renewal_due_soon`, suggest arranging recurrent training.
- If the script returns `valid`, state the expiration date and remaining days.
- Do not invent training types or validity periods that are not in the table.
