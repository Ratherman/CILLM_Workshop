# Invoice Policy Index

Use this index to select the exact invoice-processing reference file. Do not load all reference files by default.

| Query Type | User Keywords | Reference File | Notes |
|---|---|---|---|
| Triplicate invoice | 三聯式發票、三聯發票、公司統編、買受人統編、營業稅、未稅金額 | `references/ref_1_triplicate_invoice.md` | Use when the document is a company reimbursement invoice with buyer company name or tax ID. |
| Duplicate invoice | 二聯式發票、二聯發票、一般發票、沒有統編、消費發票 | `references/ref_2_duplicate_invoice.md` | Use when the invoice is a general consumer invoice or lacks buyer tax ID. |
| Transportation receipt | 交通費、計程車、高鐵、台鐵、捷運、停車費、過路費、uber、ride-hailing | `references/ref_3_transportation_receipt.md` | Use for transportation-related reimbursement documents. |
| Other receipt | 手寫收據、國外收據、截圖、付款證明、訂單確認、看不出是哪種憑證、其它 | `references/ref_4_other_receipt.md` | Use when the document is not a standard invoice or transport receipt. |
| Electronic invoice certificate | 電子發票證明聯、電子發票紙本、超商電子發票、店家電子發票 | `references/ref_5_electronic_invoice_certificate.md` | Use when the user has a printed electronic invoice certificate copy. |
| Cloud or carrier invoice | 雲端發票、手機載具、會員載具、自然人憑證、發票平台截圖 | `references/ref_6_cloud_carrier_invoice.md` | Use when the invoice exists in a carrier or cloud invoice platform. |
| Foreign currency receipt | 國外發票、外幣收據、海外收據、外幣付款、exchange rate、foreign receipt | `references/ref_7_foreign_currency_receipt.md` | Use for overseas or foreign-currency reimbursement proof. |
| E-commerce invoice or order | 線上購物、電商、訂單確認、momo、PChome、Amazon、網購發票 | `references/ref_8_ecommerce_invoice.md` | Use when the proof is an online order, marketplace receipt, or e-commerce invoice. |
| Credit card slip | 信用卡簽單、刷卡證明、信用卡明細、card slip、bank statement | `references/ref_9_credit_card_slip.md` | Use when the user only has card payment proof or asks whether card slips are enough. |
| Meal or entertainment receipt | 餐費、交際費、業務餐、招待客戶、聚餐、餐廳發票 | `references/ref_10_meal_entertainment_receipt.md` | Use for meal or hospitality reimbursement documents. |
| Lost invoice supplement | 發票遺失、正本不見、補件、遺失證明、付款證明替代 | `references/ref_11_lost_invoice_supplement.md` | Use when the original invoice is missing or the user asks how to supplement documents. |
| Invoice error or reissue | 統編錯、金額錯、日期錯、品名錯、發票錯誤、重開發票、作廢重開 | `references/ref_12_invoice_error_reissue.md` | Use when the invoice has incorrect fields or may need reissue. |

## Routing Rules

- If the user explicitly says the document type, select the matching reference.
- If the user only says "發票" and mentions company tax ID, select triplicate invoice.
- If the user only says "發票" and says there is no tax ID, select duplicate invoice.
- If the user mentions route, trip, taxi, train, parking, toll, or transport, select transportation receipt.
- If the user mentions a printed electronic invoice certificate copy, select electronic invoice certificate.
- If the user mentions cloud invoice, mobile carrier, member carrier, or invoice app screenshot, select cloud or carrier invoice.
- If the user mentions overseas vendors, foreign currency, or exchange rate, select foreign currency receipt.
- If the user mentions online shopping, marketplace orders, or order confirmation, select e-commerce invoice.
- If the user only has a credit-card slip or card statement, select credit card slip.
- If the user mentions meals, business meals, clients, hospitality, or restaurants, select meal or entertainment receipt.
- If the original invoice is lost, select lost invoice supplement.
- If invoice fields are wrong, select invoice error or reissue.
- If the document type cannot be determined, ask one clarifying question instead of loading multiple detailed references.
