# Ref 1: 三聯式發票處理

三聯式發票通常用於公司報帳或需買受人統編的交易。

## Required Fields

- 發票號碼
- 發票日期
- 賣方名稱
- 賣方統一編號
- 買受人公司名稱
- 買受人統一編號
- 品名或摘要
- 未稅金額、營業稅、總金額

## Handling Rules

- If buyer tax ID is missing, ask the user to confirm whether the invoice must be reissued.
- If the tax amount does not match the total amount, ask the user to verify the invoice.
- If item description is too vague, ask the user to add reimbursement purpose.
- If all required fields are present, say it appears ready for reimbursement review.

## Clarifying Question

If required fields are missing, ask first for the missing buyer company name or buyer tax ID, because that is the most important triplicate-invoice distinction.
