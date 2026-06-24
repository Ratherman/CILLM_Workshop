---
name: invoice-process-with-refs
description: Demo skill for reimbursement document and invoice processing with on-demand references. Use when the user asks whether a document can be used for reimbursement, what fields are missing, or how to handle receipts/invoices such as Taiwan triplicate invoices, duplicate invoices, transportation receipts, electronic invoice certificate copies, cloud or carrier invoices, foreign receipts, e-commerce orders, credit card slips, card payment proofs, meal or entertainment receipts, lost invoices, invoice errors, missing item details, missing tax ID, or unclear receipt documents. It loads only the relevant reference file.

capabilities:
  - invoice_classification
  - invoice_required_fields_check
  - reimbursement_document_guidance

response_language: zh-TW

references:
  invoice_policy_index:
    path: ./references/invoice_policy_index.md
    description: Routing index used to select the exact invoice-processing reference based on document type and user intent.

  triplicate_invoice:
    path: ./references/ref_1_triplicate_invoice.md
    description: Processing rules for Taiwan-style triplicate invoices used for company reimbursement.

  duplicate_invoice:
    path: ./references/ref_2_duplicate_invoice.md
    description: Processing rules for duplicate invoices and general consumer invoices.

  transportation_receipt:
    path: ./references/ref_3_transportation_receipt.md
    description: Processing rules for taxi, train, high-speed rail, parking, toll, ride-hailing, and other transportation-related receipts.

  other_receipt:
    path: ./references/ref_4_other_receipt.md
    description: Processing rules for handwritten receipts, foreign receipts, screenshots, payment slips, online order confirmations, and unclear documents.

  electronic_invoice_certificate:
    path: ./references/ref_5_electronic_invoice_certificate.md
    description: Processing rules for electronic invoice certificate copies issued by stores or platforms.

  cloud_carrier_invoice:
    path: ./references/ref_6_cloud_carrier_invoice.md
    description: Processing rules for cloud invoices, mobile carrier invoices, member carrier invoices, and invoice platform screenshots.

  foreign_currency_receipt:
    path: ./references/ref_7_foreign_currency_receipt.md
    description: Processing rules for foreign invoices, overseas receipts, and foreign-currency payment proofs.

  ecommerce_invoice:
    path: ./references/ref_8_ecommerce_invoice.md
    description: Processing rules for online shopping orders, e-commerce invoices, marketplace receipts, and order confirmations.

  credit_card_slip:
    path: ./references/ref_9_credit_card_slip.md
    description: Processing rules for credit card slips, card payment proofs, and bank card transaction records.

  meal_entertainment_receipt:
    path: ./references/ref_10_meal_entertainment_receipt.md
    description: Processing rules for meal expenses, business meals, entertainment receipts, and hospitality reimbursement documents.

  lost_invoice_supplement:
    path: ./references/ref_11_lost_invoice_supplement.md
    description: Processing rules for lost invoices, missing original documents, replacement proof, and reimbursement supplement handling.

  invoice_error_reissue:
    path: ./references/ref_12_invoice_error_reissue.md
    description: Processing rules for invoice errors, wrong tax ID, wrong amount, wrong date, wrong item name, and reissue handling.

scripts: {}
---

# Invoice Process With References

This skill demonstrates reference-based, on-demand invoice processing.

Use Traditional Chinese by default. Help the user classify the reimbursement document type, identify required fields, and explain the next handling step. Do not claim these are official company policies.

## Workflow

1. Use `invoice_policy_index` first to select the relevant reference file.
2. Load only the reference file needed for the user's document type.
3. Answer only from the loaded reference content and this skill's general workflow.
4. If the document type is unclear, ask one clarifying question before selecting detailed handling rules.

## Response Style

- Keep the response concise and practical.
- Use bullet points when listing missing fields.
- Do not mention internal routing, references, or scripts.
- If information is incomplete, ask only the most important clarifying question first.
