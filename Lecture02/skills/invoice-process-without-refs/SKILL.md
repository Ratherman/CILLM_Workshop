---
name: invoice-process-without-refs
description: Demo skill for reimbursement document and invoice processing without references. Use when the user asks whether a document can be used for reimbursement, what fields are missing, or how to handle receipts/invoices such as Taiwan triplicate invoices, duplicate invoices, transportation receipts, electronic invoice certificate copies, cloud or carrier invoices, foreign receipts, e-commerce orders, credit card slips, card payment proofs, meal or entertainment receipts, lost invoices, invoice errors, missing item details, missing tax ID, or unclear receipt documents. It handles all rules embedded directly in SKILL.md.

capabilities:
  - invoice_classification
  - invoice_required_fields_check
  - reimbursement_document_guidance

response_language: zh-TW

references: {}
scripts: {}
---

# Invoice Process Without References

This skill is a no-reference comparison skill. All invoice processing rules are embedded directly in this `SKILL.md`.

Use Traditional Chinese by default. Help the user classify the reimbursement document type, identify required fields, and explain the next handling step. Do not claim these are official company policies.

## Common Workflow

1. Identify the document type:
   - 三聯式發票
   - 二聯式發票
   - 交通衍生收據
   - 其它憑證
   - 電子發票證明聯
   - 雲端發票 / 載具發票
   - 國外發票 / 外幣收據
   - 線上購物訂單 / 電商發票
   - 信用卡簽單 / 刷卡證明
   - 餐費 / 交際費憑證
   - 發票遺失 / 補件處理
   - 發票錯誤 / 重開處理
2. Check whether the required fields are present.
3. Tell the user what is missing, or explain that the document appears ready for reimbursement review.
4. If the document type is unclear, ask one clarifying question.

## 三聯式發票處理規則

三聯式發票通常用於公司報帳或需買受人統編的交易。

Required fields:

- 發票號碼
- 發票日期
- 賣方名稱
- 賣方統一編號
- 買受人公司名稱
- 買受人統一編號
- 品名或摘要
- 未稅金額、營業稅、總金額

Handling rules:

- If buyer tax ID is missing, ask the user to confirm whether the invoice must be reissued.
- If the tax amount does not match the total amount, ask the user to verify the invoice.
- If item description is too vague, ask the user to add reimbursement purpose.
- If all required fields are present, say it appears ready for reimbursement review.

## 二聯式發票處理規則

二聯式發票通常用於一般消費，可能沒有買受人統編。

Required fields:

- 發票號碼
- 發票日期
- 賣方名稱或店家資訊
- 金額
- 消費品項或可辨識交易內容

Handling rules:

- If buyer company name or tax ID is absent, do not automatically reject it; explain that duplicate invoices may be acceptable depending on reimbursement rules.
- If item detail is missing, ask the user to provide purchase purpose.
- If the invoice only shows total amount, ask whether supporting detail is available.
- If all core fields are present, say it can be submitted with a clear reimbursement reason.

## 交通衍生收據處理規則

交通衍生收據 includes taxi receipts, train tickets, high-speed rail tickets, parking receipts, toll receipts, ride-hailing receipts, and public transportation payment records.

Required fields:

- 交通日期
- 交通類型
- 起訖地點 or route description
- 金額
- Business purpose or trip reason

Handling rules:

- If origin and destination are missing, ask the user to add route information.
- If only a credit-card statement exists, ask for the original transportation receipt if available.
- If the receipt is for parking or tolls, ask the user to connect it to the business trip or visit.
- If the amount is unclear, ask for proof of payment.

## 其它憑證處理規則

其它憑證 includes handwritten receipts, foreign receipts, screenshots, online order confirmations, payment slips, or unclear documents.

Required fields:

- Transaction date
- Vendor or payee
- Amount and currency
- Purchase content or service description
- Reason why a standard invoice is unavailable

Handling rules:

- If vendor information is missing, ask for supporting evidence.
- If currency is foreign, ask for currency and exchange-rate basis.
- If it is a screenshot, ask whether it includes payment completion proof.
- If the document is unclear, ask the user to provide a clearer copy or summarize visible fields.

## 電子發票證明聯處理規則

電子發票證明聯通常由店家、超商、餐廳或平台列印，外觀可能像紙本發票，但內容來自電子發票系統。

Required fields:

- 發票號碼
- 發票日期與時間
- 賣方名稱或店家資訊
- 賣方統一編號
- 金額
- 隨機碼或電子發票識別資訊
- 品項明細或可辨識交易內容

Handling rules:

- If the certificate copy has only total amount and no item detail, ask whether a transaction detail or receipt detail is available.
- If the printed copy is faded or incomplete, ask the user to provide a clearer copy or electronic invoice lookup screenshot.
- If the invoice number or random code is missing, ask the user to verify whether it is a valid electronic invoice certificate.
- If all key fields are present, say it appears ready for reimbursement review with a clear reimbursement purpose.

## 雲端發票 / 載具發票處理規則

雲端發票或載具發票 may be stored under a mobile barcode carrier, member carrier, natural person certificate, store app, or invoice platform.

Required fields:

- 發票號碼
- 發票日期
- 賣方名稱或店家資訊
- 金額
- 載具類型或平台來源
- 品項明細或交易內容
- Screenshot or export showing invoice ownership and transaction details

Handling rules:

- If the user only has a carrier barcode but no invoice detail, ask for the invoice detail page or platform screenshot.
- If the screenshot does not show invoice number, date, and amount together, ask for a complete screenshot.
- If the platform only shows winning status or donation status, ask for the transaction detail page instead.
- If the invoice is donated or assigned elsewhere, ask the user to confirm whether it can still be used for reimbursement.

## 國外發票 / 外幣收據處理規則

Foreign receipts and foreign-currency invoices are used for overseas vendors, foreign travel, international online services, or expenses paid in non-TWD currency.

Required fields:

- Transaction date
- Vendor or payee name
- Amount and currency
- Purchase content or service description
- Payment proof
- Exchange-rate basis or reimbursement currency explanation
- Business purpose in Traditional Chinese

Handling rules:

- If currency is missing, ask the user to confirm the currency.
- If the amount is foreign currency, ask for the exchange-rate basis used for reimbursement.
- If the receipt language is not Chinese or English, ask the user to summarize vendor, date, amount, and purpose.
- If the document only proves payment but not purchase content, ask for invoice, receipt, or order detail.

## 線上購物訂單 / 電商發票處理規則

E-commerce reimbursement documents may include online order confirmations, marketplace invoices, platform receipts, seller invoices, payment records, or delivery records.

Required fields:

- Order number
- Order date
- Platform or seller name
- Purchased item or service description
- Amount
- Payment completion proof
- Invoice or receipt if available
- Delivery or fulfillment status when relevant

Handling rules:

- Order confirmation alone does not always prove payment completion; ask for payment proof if missing.
- If the order contains personal and business items together, ask the user to identify the reimbursable items and amount.
- If the invoice is issued separately from the order, ask the user to attach both invoice and order detail.
- If the platform is overseas, also apply foreign-currency receipt checks when currency is not TWD.

## 信用卡簽單 / 刷卡證明處理規則

Credit card slips and card statements usually prove payment, but they may not prove what was purchased.

Required fields:

- Transaction date
- Merchant name
- Card payment amount
- Authorization or transaction record when available
- Matching invoice, receipt, or purchase detail
- Business purpose

Handling rules:

- Do not treat a card slip alone as complete purchase detail unless it clearly includes item information.
- If only the card slip is available, ask for the invoice, receipt, order detail, or merchant-issued document.
- If the card statement masks merchant detail, ask for supporting proof from the merchant.
- If the amount differs from the invoice because of tip, exchange rate, or installment, ask for explanation.

## 餐費 / 交際費憑證處理規則

Meal and entertainment receipts may require more context because the business purpose and participants matter.

Required fields:

- Receipt or invoice date
- Restaurant or vendor name
- Amount
- Meal purpose or business reason
- Participants or guest category when relevant
- Item detail when available
- Invoice number if the document is an invoice

Handling rules:

- If the meal purpose is missing, ask the user to provide the business reason.
- If it involves guests or clients, ask for participant context without requesting unnecessary personal data.
- If alcohol, private items, or mixed expenses appear in details, ask the user to identify reimbursable amount.
- If only a credit-card slip exists, also apply credit-card slip checks.

## 發票遺失 / 補件處理規則

Lost invoice handling applies when the original invoice, receipt, or required document is missing.

Required fields:

- What document was lost
- Transaction date
- Vendor or payee
- Amount
- Payment proof
- Purchase purpose
- Any replacement copy, platform record, or merchant reprint
- Explanation of why the original cannot be provided

Handling rules:

- If a reprint or electronic copy is available, ask the user to provide it first.
- If only payment proof exists, explain that payment proof may support the claim but may not replace purchase detail.
- If the user has no vendor information, ask for card statement, order record, or other supporting evidence.
- If the document was a formal invoice with wrong or missing information, consider whether reissue handling is more appropriate.

## 發票錯誤 / 重開處理規則

Invoice error handling applies when invoice fields are incorrect or inconsistent.

Common error types:

- 買受人統一編號錯誤
- 買受人公司名稱錯誤
- 金額錯誤
- 發票日期錯誤
- 品名或摘要錯誤
- 賣方資訊錯誤
- 稅額與總額不一致

Handling rules:

- If buyer tax ID is wrong, ask the user to confirm whether the vendor can void and reissue the invoice.
- If amount, tax, or total is wrong, ask the user to verify with the vendor before reimbursement review.
- If date is wrong, ask whether it affects the reimbursement period or transaction proof.
- If item description is wrong or too vague, ask whether the vendor can correct or provide supporting detail.
- If the invoice has already been voided, ask for the reissued invoice rather than using the old one.

## Response Style

- Keep the response concise and practical.
- Use bullet points when listing missing fields.
- Do not mention internal routing, references, or scripts.
- If information is incomplete, ask only the most important clarifying question first.
