---
name: hr-training-validity-without-scripts
description: Helps employees check whether aviation workplace training or certificate records are still valid without using scripts. Use when the user explicitly asks to test hr-training-validity-without-scripts or asks about training completion dates, validity periods, expiration dates, remaining days, renewal timing, or retraining needs. All training validity tables and date calculation instructions are embedded directly in SKILL.md.

capabilities:
  - training_validity_check
  - certificate_expiration_query
  - recurrent_training_due_query

response_language: zh-TW

references: {}
scripts: {}
---

# HR Training Validity Without Scripts

This demo skill answers training or certificate validity questions without using scripts. All lookup data and calculation logic are embedded in this `SKILL.md`.

Use Traditional Chinese by default. Do not claim these are official company rules. This skill is intentionally less deterministic than the script-based version because the LLM must perform date calculation itself.

## Supported Training Table

| Training ID | Chinese Name | Valid Months | Renewal Notice Days | Keywords |
|---|---:|---:|---:|---|
| `dangerous_goods` | 危險物品訓練 | 24 | 60 | 危險物品, DG, dangerous goods |
| `aviation_security` | 航空保安訓練 | 12 | 45 | 航空保安, 保安訓練, security |
| `safety_management_system` | 安全管理系統訓練 | 36 | 90 | 安全管理, SMS, safety management |
| `ground_service` | 地勤服務訓練 | 18 | 60 | 地勤服務, 旅客服務, ground service |
| `ramp_safety` | 機坪安全訓練 | 12 | 45 | 機坪安全, ramp safety, apron |
| `maintenance_human_factors` | 修護人因訓練 | 24 | 60 | 修護人因, 人因訓練, maintenance human factors |
| `cabin_safety_recurrent` | 空服安全複訓 | 12 | 60 | 空服安全, 客艙安全, cabin safety, 安全複訓 |

## Manual Calculation Rules

1. Identify the training type from the user's wording and the supported training table.
2. Read the completion date from the user.
3. If the user provides an as-of date, use it. Otherwise use today's date from the runtime context if available.
4. Calculate `valid_until` by adding `Valid Months` to the completion date.
   - Example: 2025-08-01 plus 24 months = 2027-08-01.
   - If the original day does not exist in the target month, use the last day of the target month.
   - Example: 2025-01-31 plus 1 month = 2025-02-28.
5. Calculate `days_remaining` as `valid_until - as_of_date`.
6. Determine status:
   - If `days_remaining < 0`, status is `expired`.
   - If `0 <= days_remaining <= Renewal Notice Days`, status is `renewal_due_soon`.
   - If `days_remaining > Renewal Notice Days`, status is `valid`.

## Required Information

- Training type or training name.
- Completion date.
- Optional as-of date.

If training type is unclear, ask one clarifying question. If completion date is missing, ask for the completion date.

## Response Rules

- Respond in Traditional Chinese.
- Show the matched training name, completion date, validity period, calculated expiration date, and status.
- If the result is `valid`, state the expiration date and remaining days.
- If the result is `renewal_due_soon`, state the expiration date and suggest arranging recurrent training.
- If the result is `expired`, state the expiration date and how many days have passed since expiration.
- Do not invent training types or validity periods outside the supported table.
- If date calculation is uncertain, state the assumption clearly instead of pretending certainty.

## Example

User: 我 2025/08/01 完成危險物品訓練，2026/06/24 還有效嗎？

Expected reasoning:

- Training type: `dangerous_goods`
- Valid months: 24
- Completion date: 2025-08-01
- As-of date: 2026-06-24
- Valid until: 2027-08-01
- Status: valid

Response style:

您的危險物品訓練完成日是 2025-08-01，依本 demo 規則效期為 24 個月，因此效期至 2027-08-01。以 2026-06-24 來看仍在有效期限內，距離到期還有一段時間，目前不需要立即安排複訓。
