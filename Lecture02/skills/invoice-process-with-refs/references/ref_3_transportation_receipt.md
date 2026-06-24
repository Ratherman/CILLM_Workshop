# Ref 3: 交通衍生收據處理

交通衍生收據 includes taxi receipts, train tickets, high-speed rail tickets, parking receipts, toll receipts, ride-hailing receipts, and public transportation payment records.

## Required Fields

- 交通日期
- 交通類型
- 起訖地點 or route description
- 金額
- Business purpose or trip reason

## Handling Rules

- If origin and destination are missing, ask the user to add route information.
- If only a credit-card statement exists, ask for the original transportation receipt if available.
- If the receipt is for parking or tolls, ask the user to connect it to the business trip or visit.
- If the amount is unclear, ask for proof of payment.

## Clarifying Question

If route information is missing, ask the user for the origin, destination, and business purpose of the trip.
