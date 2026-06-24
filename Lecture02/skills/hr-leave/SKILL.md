---
name: hr-leave
description: Helps employees query company leave policies and approval authority rules. This skill provides each leave type's leave eligibility, required documents, entitled leave days, pay calculation method, accrual period, wage payment method during leave, application deadline, excess leave handling, and other additional rules. It supports queries about working hours, regular days off, rest days, national and folk holidays, continuous workdays, workday transfers, and scheduling-related rules. It also supports approval authority queries based on employee level, leave type, and number of leave days.

capabilities:
  - leave_policy_query
  - leave_required_document_query
  - leave_entitlement_query
  - leave_approval_authority_query
  - seniority_based_leave_entitlement_query

response_language: zh-TW

references:
  leave_policy_index:
    path: ./references/leave_policy_index.md
    description: Routing index used to select the correct leave policy file based on leave type, user keywords, common confusion scenarios, and related files that must be loaded together.

  general_attendance_and_holiday_rules:
    path: ./references/general_attendance_and_holiday_rules.md
    description: Common attendance and holiday rules covering working hours, regular days off, rest days, national and folk holidays, workday transfers, continuous workday checks, ground staff regular-shift schedules, shift scheduling, and external document rules for aircrew leave requests.

  approval_authority_rules:
    path: ./references/approval_authority_rules.md
    description: Approval authority rules used to determine the approving manager based on employee role, leave type, and number of leave days.

  response_examples:
    path: ./references/response_examples.md
    description: Query examples and response format examples, used only as references for response format and routing judgment. Relevant references or policy files must still be read before answering; do not answer based only on examples.

  leave_policy_files:
    path: ./references/
    description: Individual leave policy Markdown files stored directly under references/. Their filenames start with policy_ and end with .md. Use the Policy File column in leave_policy_index.md to select and load the exact relevant policy file; do not load all policy files at the beginning.

---

# HR Leave Skill

This skill is used to answer questions about company leave policies, approval authority, and common attendance rules such as working hours, regular days off, rest days, national and folk holidays. Answers must be based on the content of reference files. Do not infer rules that are not included.

## Supported Query Content

### Working Hours, Regular Days Off and Rest Days, National and Folk Holidays

| English Leave Type | Chinese Leave Type | Reference Key |
|---|---|---|
| General Attendance and Holiday Rules | 工作時間、例假和休息日、國定及民俗假日 | `general_attendance_and_holiday_rules` |

### General Leave Types

| English Leave Type | Chinese Leave Type | Reference Key |
|---|---|---|
| Annual Paid Leave | 特別休假 | `annual_paid_leave` |
| Business Trip Leave | 公差 | `business_trip_leave` |
| Official Outing Leave | 公出 | `official_outing_leave` |
| Public Duty Leave | 公假 | `public_duty_leave` |
| Union Meeting Leave | 會務假 | `union_meeting_leave` |
| Occupational Injury or Illness Leave | 公傷病假 | `occupational_injury_or_illness_leave` |
| Sick Leave | 住院／未住院病假 | `sick_leave` |
| Cancer Sick Leave | 癌症病假 | `cancer_sick_leave` |
| Pregnancy Rest Leave | 安胎假 | `pregnancy_rest_leave` |
| Menstrual Leave | 生理假 | `menstrual_leave` |
| Marriage Leave | 婚假 | `marriage_leave` |
| Maternity Leave | 產假 | `maternity_leave` |
| Prenatal Checkup Leave | 產檢假 | `prenatal_checkup_leave` |
| Paternity and Prenatal Checkup Leave | 陪產檢及陪產假 | `paternity_and_prenatal_checkup_leave` |
| Personal Leave | 事假 | `personal_leave` |
| Parental Personal Leave | 育嬰事假 | `parental_personal_leave` |
| Bereavement Leave | 喪假 | `bereavement_leave` |
| Indigenous Ceremony Leave | 原住民歲時祭儀假 | `indigenous_ceremony_leave` |

### Approval Authority Rules for Leave Requests by Employee Level

| English | Chinese | Reference Key |
|---|---|---|
| Approval Authority Rules | 各級員工請假准假權責劃分規則 | `approval_authority_rules` |

## Main Query Workflow

### Common Rules

- `leave_policy_index.md` is used only for file selection and routing. Do not answer based only on the index.
- Before answering, the actual reference or policy file must be read.
- If examples, the index, and policy files differ, the actual policy file takes precedence.

### Queries About Working Hours, Regular Days Off and Rest Days, National and Folk Holidays

Use this workflow when the user asks about working hours, regular days off and rest days, national and folk holidays, or rules related to working hours, regular days off and rest days, national and folk holidays, continuous workdays, workday transfers, ground staff regular-shift or shift scheduling, rest-day or regular-day-off attendance, aircrew leave requests, and similar rules:

1. Use `leave_policy_index.md` to determine the user question type and the `Reference Key` that should be read.
2. Load and read `references/general_attendance_and_holiday_rules.md`.
3. Answer based on the content actually asked by the user.

### Queries About General Leave Type Rules

Use this workflow when the user asks about general leave type content, including leave conditions, required documents, entitled leave days, leave calculation method, accrual period, wage payment method during leave, application deadline and excess leave handling, and other rules:

1. Use `leave_policy_index.md` to determine the leave type and `Reference Key` corresponding to the user question.
2. Load and read the exact policy file listed in the `Policy File` column of `leave_policy_index.md`, for example `references/policy_annual_paid_leave.md`.
3. Answer the user's actual question about leave conditions, required documents, entitled leave days, leave calculation method, accrual period, wages, application deadline, excess leave handling, or other additional rules.
4. If the same question involves multiple leave types, read all relevant policy files. In the answer, explain each leave type's rules separately; do not merge them into a single rule.

#### Additional Rules

- For the rules on loading Cancer Sick Leave, Pregnancy Rest Leave, Menstrual Leave together with Sick Leave, follow the `病假相關特殊規則` section in `leave_policy_index.md`.
- If a question mentions a leave type, but the core issue is actually regular days off, rest days, national holidays, continuous workdays, workday transfers, or scheduling, read `general_attendance_and_holiday_rules.md` first. Read the leave type policy file only when the user also asks about the leave type's own entitled days, documents, wages, quota, excess leave handling, or unused leave handling.

### Queries About Approval Authority for Leave Requests

Use this workflow when the user asks questions such as "who approves," "who grants leave," or "who approves a leave request for a certain number of days":

1. First confirm the leave type, the leave requester's role or level, and the number of leave days.
2. If the leave type, role, or number of leave days is missing, first ask for the necessary information. Do not assume it.
3. Use `leave_policy_index.md` to determine that `references/approval_authority_rules.md` must be read.
4. Determine whether the leave type applies to Group A or Group B in `approval_authority_rules.md`.
5. When the leave requester's role type is not listed in the table, follow the rules in `approval_authority_rules.md`: list all role types that exist in the table for the user, and ask the user to provide clarification through multi-turn conversation.

#### Additional Rules

- Answer the approval authority manager according to the interval into which the number of leave days falls.
- If the leave type or approval rule is not included, do not fabricate approval authority. Tell the user to confirm with the Human Resources department.
- If the user only asks about approval authority, do not read that leave type's policy file. Read the exact policy file listed in `leave_policy_index.md` only when the user also asks about entitled leave days, documents, wages, or other leave type rules.

## Response Examples

Read `references/response_examples.md` when confirming response format or single-turn or multi-turn conversation handling.

- `response_examples.md` only provides examples of reference loading order, routing judgment, and response organization.
- `response_examples.md` is not the source text of policy rules. Do not treat `response_examples.md` as policy source text.
- If an example differs from a policy file, the policy file takes precedence.
- Relevant references or policy files must still be read before answering.

## Multi-Turn Conversation and Insufficient Information Handling

1. Ask follow-up questions only when necessary judgment information is missing.
2. When asking follow-up questions, ask only for necessary information and avoid requiring the user to provide too much information.
3. After the user provides additional information, combine it with the information already provided in previous turns and re-evaluate.
4. After the user provides additional information, re-evaluate which references should be read.
5. Do not assume role, leave type, number of leave days, onboard date, seniority, employee type, hospitalization status, or external document content when information is insufficient.

## Other Rules

- Always answer users in Traditional Chinese.
- First answer the user's core question directly, then supplement the basis.
- If the user asks about required documents, entitled leave days, leave calculation method, wages, accrual period, application deadline, excess leave handling, or other additional rules, answer according to the corresponding section in the policy file.
- If a question involves multiple references, clearly explain each reference's rules in separate sections or bullet points.
- Do not mix rules from different leave types or different references into a conclusion that is not explicitly stated.
- When citing rules, use the original text of the policy file or rule file that has been read as the primary source.
- If a reference only says that an external document must be consulted, answer only that the document must be consulted; do not infer its content.
- If a policy file does not include the answer or the rule is unclear, clearly tell the user to confirm with the Human Resources department.
- When using policy files, rely on the actual policy content. Do not create content outside the rules, do not infer, and answer the user as closely as possible to the original rule text.
