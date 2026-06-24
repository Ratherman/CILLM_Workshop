# Ref 2: 二聯式發票處理

二聯式發票通常用於一般消費，可能沒有買受人統編。

## Required Fields

- 發票號碼
- 發票日期
- 賣方名稱或店家資訊
- 金額
- 消費品項或可辨識交易內容

## Handling Rules

- If buyer company name or tax ID is absent, do not automatically reject it; explain that duplicate invoices may be acceptable depending on reimbursement rules.
- If item detail is missing, ask the user to provide purchase purpose.
- If the invoice only shows total amount, ask whether supporting detail is available.
- If all core fields are present, say it can be submitted with a clear reimbursement reason.

## Clarifying Question

If the invoice has only an amount and no item details, ask the user to provide the purchase purpose or supporting detail.
