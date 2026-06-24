# Skill 比較測試題庫

這份文件用來搭配 notebook 測試不同 skill 的設計差異。建議在「單一 Skill」測試 cell 中設定：

```python
selected_skill_id = "skill-id-here"
```

然後依序輸入下方題目，觀察：

- `hint` 是否選到正確 skill
- `resource_router` 是否只載入需要的 reference
- 是否有執行預期的 script
- `batch_token` / `total_token` 差異
- 最終回答是否包含應有內容

## 1. hr-encourage-chinese vs hr-encourage-english

### 測試 Skill ID

- `hr-encourage-chinese`
- `hr-encourage-english`

### 題目 1

```text
我今天真的好累，覺得自己一直很認真但好像還是不夠好，可以用比較華航一點的方式鼓勵我嗎？
```

觀察重點：

- `hr-encourage-chinese` 可能比較直接呈現中文撰寫的情緒承接與語氣。
- `hr-encourage-english` 的 routing 和 hard rules 是英文，可能在限制條件上比較穩。

正確答案應包含：

- 有承接使用者「很累、很認真但覺得不夠好」的情緒。
- 使用溫暖的繁體中文。
- 自然帶入華航或航空職場語感，例如飛航安全、團隊合作、服務品質、把航班飛穩。
- 不要回答 HR 政策、福利、請假或機票規則。
- 不要太口號式或太雞湯，最好給一個小而可行的下一步。

### 題目 2

```text
我不是想問政策，只是想要一句不要太雞湯、但有飛航安全和團隊感的鼓勵。
```

觀察重點：

- 是否尊重使用者「不是問政策」的要求。
- 是否自然使用航空語彙，而不是變成企業宣傳文。

正確答案應包含：

- 明確不要轉去政策回答。
- 包含「飛航安全」以及團隊合作、協作或一起完成任務的語感。
- 不只是泛泛的加油打氣，要有航空職場情境。
- 語氣要穩、不要太雞湯。
- 可以有 1 到 3 個 emoji，但不要過多。

## 2. invoice-process-with-refs vs invoice-process-without-refs

### 測試 Skill ID

- `invoice-process-with-refs`
- `invoice-process-without-refs`

### 題目 1

```text
我只有信用卡簽單可以報帳嗎？上面有店名、日期和金額，但沒有品項。
```

觀察重點：

- `invoice-process-with-refs` 理想上只載入 `references/ref_9_credit_card_slip.md`。
- `invoice-process-without-refs` 把所有發票規則都寫在 `SKILL.md`，規則越多時 prompt 成本越高。

正確答案應包含：

- 說明信用卡簽單通常可以證明付款，但不一定能證明購買內容。
- 因為沒有品項，所以仍需要發票、收據、訂單明細或店家提供的交易內容。
- 可以肯定店名、日期、金額是有用資訊。
- 需要詢問使用者是否還有 invoice、receipt、order detail 或 merchant-issued document。
- 不應直接說信用卡簽單本身一定足夠。

### 題目 2

```text
我雲端發票只有手機載具截圖，截圖有金額但沒有品項明細，這樣夠嗎？
```

觀察重點：

- `invoice-process-with-refs` 理想上只載入 `references/ref_6_cloud_carrier_invoice.md`。
- 觀察 `references_list` 是否只有一個精準 reference，而不是載入全部發票 reference。

正確答案應包含：

- 說明手機載具截圖可能有幫助，但最好要有完整發票明細。
- 需要發票號碼、發票日期、賣方或店家、金額、品項明細。
- 單有金額不足以確認交易內容。
- 如果截圖不完整，應請使用者提供雲端發票明細頁或完整平台截圖。
- 不要在題意清楚時錯誤導向信用卡簽單或其它憑證。

## 3. hr-training-validity-with-scripts vs hr-training-validity-without-scripts

### 測試 Skill ID

- `hr-training-validity-with-scripts`
- `hr-training-validity-without-scripts`

### 題目 1

```text
我 2025/07/20 完成機坪安全訓練，以 2026/06/24 來看還有效嗎？需要安排複訓了嗎？
```

觀察重點：

- `hr-training-validity-with-scripts` 應該執行 `training_validity_lookup`。
- script arguments 應該包含：
  - `training_type=ramp_safety`
  - `completion_date=2025-07-20`
  - `as_of_date=2026-06-24`
- script 結果應穩定給出：
  - `valid_until=2026-07-20`
  - `days_remaining=26`
  - `status=renewal_due_soon`
- `hr-training-validity-without-scripts` 需要由 LLM 自己算日期，可比較它是否穩定。

正確答案應包含：

- 辨識訓練類型為「機坪安全訓練」或 `ramp_safety`。
- 完成日是 `2025-07-20`。
- 查核日是 `2026-06-24`。
- 效期到 `2026-07-20`。
- 剩餘 `26` 天。
- 狀態是仍有效，但已進入提醒或應安排複訓的期間。
- script 版 trace 應該看得到 `training_validity_lookup`。

### 題目 2

```text
我 2024/01/01 完成航空保安訓練，以 2026/06/24 來看是不是過期了？
```

觀察重點：

- `hr-training-validity-with-scripts` 應該執行 `training_validity_lookup`。
- script arguments 應該包含：
  - `training_type=aviation_security`
  - `completion_date=2024-01-01`
  - `as_of_date=2026-06-24`
- script 結果應穩定給出：
  - `valid_until=2025-01-01`
  - `status=expired`
  - `days_remaining` 為負數
- without-script 版比較可能在天數計算上不穩。

正確答案應包含：

- 辨識訓練類型為「航空保安訓練」或 `aviation_security`。
- 完成日是 `2024-01-01`。
- 查核日是 `2026-06-24`。
- 效期到 `2025-01-01`。
- 明確說明以 `2026-06-24` 來看已過期。
- 最好能說明已過期 `539` 天，或至少指出剩餘天數為負數。
- 建議安排重新訓練或複訓。

## 4. hr-free-ticket 可回答題目

### 測試 Skill ID

- `hr-free-ticket`

### 題目 1

```text
現職員工年資 5 年，ID00 免費機票有幾點？
```

觀察重點：

- 應該選到 `hr-free-ticket`。
- 理想上應執行 `employee_free_ticket_points_lookup`。

正確答案應包含：

- 辨識這是現職員工 ID00 免費機票點數查詢。
- 使用 `employee_free_ticket_points_lookup`，不要手動讀 JSON 表格推算。
- 明確指出年資是 `5 年`。
- 提供 script 回傳的點數結果。
- 如有載入政策 reference，可補充 ID00 相關背景，但不可自行發明規則。

### 題目 2

```text
退休員工還可以使用 ID00 或有價優待票嗎？主要規則是什麼？
```

觀察重點：

- 應載入 retired employee ticket 相關 reference。
- 不應使用 reference 之外的規則自行推測。

正確答案應包含：

- 只根據退休員工機票 reference 說明。
- 如果同時談到 ID00 和有價優待票，要清楚區分兩者。
- 提及 reference 中有明載的資格、核予、使用或申請概念。
- 若沒有 script 或 reference 支援，不要自行說出精確額度或次數。
- 若有價優待票額度需要更多條件，應追問缺少資訊，而不是猜。

### 題目 3

```text
眷屬返台探親 ID00R1 和眷屬搬遷 ID00R1 的使用情境有什麼差別？
```

觀察重點：

- 應同時載入兩個眷屬相關 policy references。
- 適合測試 multi-reference selection。

正確答案應包含：

- 清楚比較 `dependent_home_visit_ID00R1` 和 `dependent_relocation_ID00R1`。
- 說明兩者情境不同：返台探親 vs 搬遷或調派相關旅程。
- 分別說明兩個 reference 裡的適用情境或資格差異。
- 不要把兩份政策混成同一條規則。
- 若具體權益取決於派駐地、眷屬身分或行程，應追問必要資訊。

## 5. hr-leave 可回答題目

### 測試 Skill ID

- `hr-leave`

### 題目 1

```text
我想請普通病假，需要附什麼證明？薪資怎麼算？
```

觀察重點：

- 應載入 sick leave policy reference。
- 應根據證明文件與薪資計算規則回答。

正確答案應包含：

- 辨識假別為普通病假。
- 說明 sick leave reference 中的證明文件規則。
- 說明 sick leave reference 中的薪資或工資處理方式。
- 若 reference 有申請期限或補件條件，也應提到。
- 不要混入癌症病假、公傷病假或其它假別，除非使用者問到。

### 題目 2

```text
產檢假可以請幾天？需要提供什麼證明？
```

觀察重點：

- 應載入 prenatal checkup leave policy reference。
- 適合測試天數與證明文件回答。

正確答案應包含：

- 辨識假別為產檢假。
- 說明 prenatal checkup leave reference 中的可請天數或額度。
- 說明需要提供的證明文件。
- 如 reference 有適用對象或條件，應一併說明。
- 不要混入產假或陪產檢及陪產假，除非使用者問到。

### 題目 3

```text
如果我是 3 職等員工，要請 2 天事假，核准主管是誰？
```

觀察重點：

- 應載入 approval authority rules。
- 如需要，也可載入 personal leave reference 作為假別背景。

正確答案應包含：

- 辨識情境為 `3 職等`、`2 天事假` 的核准權限查詢。
- 使用 approval authority rules 判斷核准主管或核決權限。
- 如果需要 personal leave reference，只用來補充假別背景。
- 若核准表需要更多角色、單位或職務資訊才能唯一判斷，應條件式說明或追問。
- 不要在 reference 無法判斷時自行猜測核准主管。
