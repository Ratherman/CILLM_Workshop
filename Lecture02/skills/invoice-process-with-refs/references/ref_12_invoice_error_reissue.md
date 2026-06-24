# Ref 12: 發票錯誤 / 重開處理

Invoice error handling applies when invoice fields are incorrect or inconsistent.

## Common Error Types

- 買受人統一編號錯誤
- 買受人公司名稱錯誤
- 金額錯誤
- 發票日期錯誤
- 品名或摘要錯誤
- 賣方資訊錯誤
- 稅額與總額不一致

## Handling Rules

- If buyer tax ID is wrong, ask the user to confirm whether the vendor can void and reissue the invoice.
- If amount, tax, or total is wrong, ask the user to verify with the vendor before reimbursement review.
- If date is wrong, ask whether it affects the reimbursement period or transaction proof.
- If item description is wrong or too vague, ask whether the vendor can correct or provide supporting detail.
- If the invoice has already been voided, ask for the reissued invoice rather than using the old one.

## Clarifying Question

Ask which field is wrong and whether the vendor can void, correct, or reissue the invoice.
