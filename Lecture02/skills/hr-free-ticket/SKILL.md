---
name: hr-free-ticket
description: Helps employees query China Airlines staff free ticket and preferential ticket rules, including ID00, ID00R1, ID00R2, free ticket points, point validity, transfer rules, route changes, cabin eligibility, current employee rules, retired employee rules, dependent relocation and home visit tickets, family service staff tickets, employee recognition award tickets, and quota lookup by identity, ticket type, cabin, employee status, and seniority.

capabilities:
  - free_ticket_policy_query
  - free_ticket_usage_query
  - current_employee_id00_query
  - retired_employee_ticket_query
  - dependent_ticket_query
  - id00_point_lookup
  - preferential_ticket_quota_lookup

response_language: zh-TW

references:

  free_ticket_policy_index:
    path: ./references/free_ticket_policy_index.md
    description: Main routing index for selecting the correct free-ticket policy reference or lookup script.

  term_definitions:
    path: ./references/term_definitions.md
    description: Definitions of staff ticket terms, identity groups, ticket types, cabins, points, transfer, validity, and other ticket vocabulary.

  free_ticket_usage_ID00:
    path: ./references/policy_free_ticket_usage_ID00.md
    description: ID00 usage rules, point calculation basics, transfer, flight sequence, child and infant tax adjustment, route change, refund, and check-in restrictions.

  free_ticket_point_usage_rules:
    path: ./references/china_airline_employee_free_ticket_point_usage_rules.md
    description: Detailed ID00 point usage rules by region and itinerary.
  
  free_air_tickets_for_current_employees_ID00:
    path: ./references/policy_free_air_tickets_for_current_employees_ID00.md
    description: Current employee ID00 eligibility, cabin, point granting, point validity, leave-without-pay handling, and ticket validity.
 
  ticket_for_family_service_staff_ID00R2:
    path: ./references/policy_ticket_for_family_service_staff_ID00R2.md
    description: Family service staff ID00R2 eligibility, yearly grant, itinerary type, change limits, and validity.
 
  employee_recognition_award_ID00R1:
    path: ./references/policy_employee_recognition_award_ID00R1.md
    description: Employee recognition award ID00R1 cabin, eligible users, grant, application period, change limits, and validity.
 
  dependent_relocation_ID00R1:
    path: ./references/policy_dependent_relocation_ID00R1.md
    description: Dependent relocation ID00R1 rules for overseas assignment, return rotation, station transfer, offline stations, and validity.
 
  dependent_home_visit_ID00R1:
    path: ./references/policy_dependent_home_visit_ID00R1.md
    description: Dependent home visit ID00R1 rules for overseas assignment, point usage, offline stations, change limits, and validity.
 
  retired_employee_tickets:
    path: ./references/policy_retired_employee_tickets.md
    description: Retired employee ID00, ID00R1, paid preferential ticket, grant period, ordering, application, and validity rules.

  response_examples:
    path: ./references/response_examples.md
    description: Response style examples only; not a source of policy truth.

scripts:
  employee_free_ticket_points_lookup:
    path: ./scripts/lookup_employee_free_ticket_points_(ID00)table.py
    description: Lookup current employee ID00 free-ticket points by seniority years. Use this script instead of reading employee_free_ticket_points_(ID00)table.json directly.
  preferential_ticket_quota_lookup:
    path: ./scripts/lookup_preferential_ticket_rules_summary_table.py
    description: Lookup preferential ticket quota by identity group, discount type, cabin, employee status, and seniority months. Use this script instead of reading preferential_ticket_rules_summary_table.json directly.
---

# HR Free Ticket Skill

Use this skill for China Airlines employee free-ticket and preferential-ticket questions. Always answer the user in Traditional Chinese.

## Supported Query Content

| Query Type | Typical User Intent | Required Reference or Script |
|---|---|---|
| Term definition | Ask what ID00, ID00R1, ID00R2, Travel Mate, CIZED, points, transfer, cabin, or other ticket terms mean. | `term_definitions` |
| ID00 usage | Ask how ID00 points are used, transfer limits, route changes, refund, child or infant ticket adjustment, or check-in restrictions. | `free_ticket_usage_ID00` |
| Detailed point usage | Ask how ID00 route points are counted by region or itinerary. | `free_ticket_point_usage_rules` plus `free_ticket_usage_ID00` when needed |
| Current employee ID00 | Ask current employee ID00 eligibility, cabin, point granting, point validity, or ticket validity. | `free_air_tickets_for_current_employees_ID00` |
| Current employee ID00 point lookup | Ask how many ID00 points a current employee has by seniority. | `employee_free_ticket_points_lookup` script |
| Family service staff ticket | Ask family service staff ID00R2 eligibility, yearly grant, route type, change limits, or validity. | `ticket_for_family_service_staff_ID00R2` |
| Employee recognition award ticket | Ask employee recognition award ID00R1 eligibility, cabin, application period, change limits, or validity. | `employee_recognition_award_ID00R1` |
| Dependent relocation ticket | Ask dependent relocation ID00R1 rules for overseas assignment, return rotation, station transfer, offline station, or validity. | `dependent_relocation_ID00R1` |
| Dependent home visit ticket | Ask dependent home visit ID00R1 rules, point usage, offline station, change limits, or validity. | `dependent_home_visit_ID00R1` |
| Retired employee ticket | Ask retired employee ID00, ID00R1, paid preferential ticket, grant period, ordering, application, or validity. | `retired_employee_tickets` |
| Preferential ticket quota | Ask how many times a user can use ID90, ID75, ID50, CIZED, ZED, or another paid preferential ticket. | `preferential_ticket_quota_lookup` script |
| Answer style | Need examples for how to structure final answers. | `response_examples` only after policy sources are selected |

## Main Query Workflow

### Common Routing Rules

1. Read `free_ticket_policy_index` first to choose the correct policy reference or lookup script.
2. Do not answer policy questions from the index alone. After routing, read the selected policy reference before answering.
3. If a question touches multiple topics, read every relevant policy reference and answer each topic separately.
4. Use `term_definitions` when the user asks about ticket vocabulary, or when a policy answer depends on a term such as ID00, ID00R1, ID00R2, CIZED, ZED, points, transfer, cabin, spouse, parents, children, Travel Mate, or retired employee.
5. Use `response_examples` only as answer-style guidance. It is not a policy source.
6. Do not expose internal implementation terms such as reference key, routing table, JSON table, or script output in ordinary employee-facing answers.

### JSON Table Handling

The JSON files under `references/` are source tables for scripts only.

- Never manually read or interpret `employee_free_ticket_points_(ID00)table.json` to answer a user.
- Never manually read or interpret `preferential_ticket_rules_summary_table.json` to answer a user.
- If a lookup requires one of these tables, run the matching script and answer from the script's JSON stdout.

### Current Employee ID00 Point Lookup

Use `scripts/lookup_employee_free_ticket_points_(ID00)table.py` when the user asks for current employee ID00 free-ticket points by seniority.

Required input:

- `seniority_years`: positive integer seniority in full years.

Command pattern:

```bash
python "skills/hr-free-ticket/scripts/lookup_employee_free_ticket_points_(ID00)table.py" <seniority_years>
```

After the script returns:

- If `"status": true`, answer with `seniority_years`, `original_points`, and `adjusted_points`.
- If `"status": false`, use the returned message to ask for the missing or corrected seniority.
- When explaining point validity, cabin, leave-without-pay handling, or ticket validity, also read `free_air_tickets_for_current_employees_ID00`.
- Do not calculate hourly employee points unless the relevant policy reference explicitly provides a calculable rule.

### Preferential Ticket Quota Lookup

Use `scripts/lookup_preferential_ticket_rules_summary_table.py` when the user asks how many times a preferential ticket can be used.

Required inputs:

- `identity_group`: for example employee and spouse, parents, children under 25, children 25 or older, dependents, or Travel Mate.
- `discount_type`: for example ID90, ID75, ID50, CIZED, or ZED.
- `cabin`: for example F, C, W, PY, or Y.
- `employee_status`: current employee or domestic retired employee.
- `seniority_months`: nonnegative integer seniority in months for current employees. This may be omitted for domestic retired employees.

Command pattern:

```bash
python "skills/hr-free-ticket/scripts/lookup_preferential_ticket_rules_summary_table.py" <identity_group> <discount_type> <cabin> <employee_status> [seniority_months]
```

If any required input is missing, ask only for the missing fields. If the user says "child" but the quota depends on age, ask whether the child is under 25 or 25 or older.

After the script returns:

- If `"status": true`, answer with the quota and the conditions that were used for lookup.
- If `"status": false`, use the returned message to ask for corrected or missing information.
- When the user asks broader retired employee policy questions, also read `retired_employee_tickets`.

### Policy Answer Workflow

For ordinary policy questions:

1. Read `free_ticket_policy_index`.
2. Select the most specific reference file. Avoid routing from generic words alone, such as cabin names or broad ticket words.
3. Read the selected policy reference.
4. If the policy reference says another local file must also be read, read that file before answering.
5. Answer directly in Traditional Chinese, starting with the practical conclusion.
6. Include conditions, limits, deadlines, validity periods, and exceptions only when they are relevant to the user's question.

### Insufficient Information Handling

Ask a concise follow-up question when the answer depends on missing information such as:

- current employee vs retired employee;
- ID00 vs ID00R1 vs ID00R2 vs paid preferential ticket;
- employee, spouse, parent, child, dependent, Travel Mate, or other identity group;
- child age group;
- cabin;
- seniority years or seniority months;
- overseas assignment, dependent relocation, dependent home visit, family service staff, employee recognition award, or retirement scenario.

If the user provides enough context to answer part of the question, answer that part first and then ask for the missing detail needed for the rest.

### External or Missing Rules

Some policy references mention external regulations that are not included in this skill. If the needed details are not in the loaded local references, do not infer them.

Use wording like:

```text
目前提供的規範內容沒有收錄這項細節，因此不能直接判定。建議補充相關規定文件，或洽人力資源部門確認。
```

## Important Separation Rules

- Do not mix current employee ID00 rules with retired employee rules.
- Do not mix ID00, ID00R1, and ID00R2 unless the user explicitly asks for comparison.
- Do not mix dependent relocation ID00R1 with dependent home visit ID00R1.
- Do not mix family service staff ID00R2 with employee recognition award ID00R1.
- Do not infer cabin eligibility from job title unless the selected policy reference explicitly contains that job title or category.
- Do not infer ZED, offline station, overseas branch, or external procedure details when the local references only point to another rule.

## Response Style

- Final answers must be in Traditional Chinese.
- Use employee-facing wording. Avoid mentioning internal files, references, routing keys, scripts, JSON, or stdout unless the user is asking about the skill implementation.
- Keep answers concise, but include the key rule, eligibility condition, quantity or points, validity period, and limitation when relevant.
- When the answer is based on a lookup result, state the lookup conditions in plain language so the user can confirm the input was correct.
- If multiple rules apply, separate them into short paragraphs or bullets.
