# Training Validity Rules

This demo skill checks whether a training or certificate record is still valid based on a completion date and a validity period table.

## General Rules

- The validity end date is calculated by adding the training type's `valid_months` to the completion date.
- If the as-of date is after the valid-until date, the status is `expired`.
- If the as-of date is within the renewal notice window before expiration, the status is `renewal_due_soon`.
- Otherwise, the status is `valid`.

## Required User Information

- Training type or training name.
- Completion date.
- Optional as-of date if the user wants to check validity on a specific date.

## Response Guidance

- Use script output for all date calculations.
- Do not manually calculate expiration dates in the LLM response.
- If the result is `valid`, state the valid-until date and days remaining.
- If the result is `renewal_due_soon`, state the valid-until date and suggest arranging recurrent training.
- If the result is `expired`, state the expiration date and how many days have passed since expiration.
