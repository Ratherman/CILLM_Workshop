# Response Examples 回答範例

- 本文件只提供 routing 與正式回答範例，不作為政策依據。

- 實際回答時，必須以讀取到的政策內容與查表結果為準，依使用者問題重新組織，不需逐字照抄範例。

## 範例 1：查詢現職員工 ID00 點數

使用者問題：

```text
我年資 5 年，ID00 有多少點？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 讀取 `policy_free_air_tickets_for_current_employees_ID00.md` 確認現職員工 ID00 點數需依對照表。
- 執行 `scripts/lookup_employee_free_ticket_points_(ID00)table.py` 查詢年資 5 年。
- 不人工解讀 `employee_free_ticket_points_(ID00)table.json`。

回答範例：

```text
依員工優待機票免票 (ID00) 點數對照表，年資 5 年的原優待機票點數為 X 點，調整配點為 Y 點。

點數使用以進點日算起一年內有效，不得累積至次年使用，也不得相互轉讓使用。
```

## 範例 2：查詢 ID00 轉機限制

使用者問題：

```text
ID00 轉機可以從中停點開始搭嗎？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 讀取 `policy_free_ticket_usage_ID00.md`。

回答範例：

```text
不可以。轉機機票不可由中停點作為啟程站點搭機。

例如 OKA-XTPE-SYD，不可搭乘 OKA-TPE 後於 TPE 做非轉機目的行為，也不可僅由 TPE 站搭機前往 SYD。若機票與實際行程不符，應重新申請開立機票。
```

## 範例 3：查詢 ID00 詳細記點方式

使用者問題：

```text
ID00 詳細記點方式怎麼算？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 讀取 `policy_free_ticket_usage_ID00.md`。
- 若問題超出第 3.1.1 的基本點數規則，再讀取 `china_airline_employee_free_ticket_point_usage_rules.md`。
- 若 `china_airline_employee_free_ticket_point_usage_rules.md` 仍為空或未收錄所需細節，不可推測。

回答範例：

```text
目前已收錄的基本規則是：亞洲至北美洲 / 歐洲 / 大洋洲地區之航點以單程四點計算，各洲區內航點間以單程二點計算；中途有轉機點之行程，取起、終點所需最大點數為計點標準。

但詳細記點方式原文指向「華航員工免費機票點數使用方式規範」。目前提供的規範內容若未包含該外部詳細規範，我不能自行推測細節。
```

## 範例 4：查詢退休後是否仍有 ID00

使用者問題：

```text
退休後還有免費票嗎？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 讀取 `policy_retired_employee_tickets.md`。
- 若使用者要查有價優待機票票種或額度，依 SKILL.md 規則使用 `scripts/lookup_preferential_ticket_rules_summary_table.py` 查詢，不直接讀取 JSON 表格。

回答範例：

```text
有，但需看是否符合退休（職）員工機票福利與核予年限。

國內退休（職）員工 ID00 點數以退休（職）日結算員工在職天數，自退休（職）生效日起算，屆滿者終止核給及使用。退休（職）後的次年，依曆年制核予退休（職）員工及其眷屬（不含滿 25 歲以上子女）退休（職）前最後一次進點之點數，之後不再逐年累加點數。
```

## 範例 5：查詢退休當年度未用完點數

使用者問題：

```text
退休當年還沒用完的 ID00 點數可以用嗎？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 讀取 `policy_retired_employee_tickets.md`。

回答範例：

```text
可以。員工及其眷屬於退休（職）日起至當年 12 月 31 日，仍可申請退休（職）生效日前未用畢之點數。

這段期間所開立的機票效期自開票日起一年有效；次年 1 月 1 日起，則按退休（職）員工規定申請 ID00 機票。
```

## 範例 6：查詢退休排序

使用者問題：

```text
退休前開的票，退休後搭乘是用在職排序還是退休排序？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 讀取 `policy_retired_employee_tickets.md`。

回答範例：

```text
退休（職）生效日前所開立之機票，使用時為在職排序。

如果是在退休（職）生效日至當年 12 月 31 日前所開立的機票，使用時為退休排序。
```

## 範例 7：查詢服務年資滿 20 年退休 ID00R1

使用者問題：

```text
服務滿 20 年退休，可以申請 ID00R1 嗎？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 讀取 `policy_retired_employee_tickets.md`。

回答範例：

```text
可以，但有條件。服務年資滿 20 年以上員工，得於退休（職）生效日後，使用退休（職）當年度未用盡之點數，向人力處申請本人及其配偶之 ID00R1 各一張。

如果退休（職）當年度已將在職時的點數用罄或無點數，則不予辦理。12 月退休、退職者，可遞延至次年 1 月 31 日以前申請及開票。
```

## 範例 8：查詢外派眷屬依親票效期

使用者問題：

```text
外派眷屬依親票效期多久？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 讀取 `policy_dependent_relocation_ID00R1.md`。

回答範例：

```text
眷屬依親 ID00R1 機票效期為自線上開票日起三個月內有效。
```

## 範例 9：比較依親票與探親票

使用者問題：

```text
外派眷屬探親票和依親票差在哪？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 同時讀取 `policy_dependent_relocation_ID00R1.md` 與 `policy_dependent_home_visit_ID00R1.md`。

回答範例：

```text
兩者都是 ID00R1，但用途與效期不同。

眷屬依親票用於員工奉派國外機構、輪調返國或外站調派其他外站等情境，通常需於人事通報發布生效日起一年內申請，效期為自線上開票日起三個月內有效。

眷屬探親票用於外派期間眷屬探親，每年以進點日一年內申請，並使用外派員工眷屬現有點數，效期為自線上開票日起一年有效。
```

## 範例 10：查詢優待機票額度

使用者問題：

```text
ID75 我小孩 25 歲以上可以用幾次？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 確認缺少員工狀態、艙等與年資月數時，先追問。
- 資訊齊全後，依 SKILL.md 規則使用 `scripts/lookup_preferential_ticket_rules_summary_table.py` 查詢 `preferential_ticket_rules_summary_table.json`。

回答範例：

```text
這題需要先確認員工狀態、艙等與年資月數，才能查優待機票規定概要表。請補充你要查的是現職員工或退休（職）員工、艙等，以及年資月數。
```

## 範例 11：缺少外部規範時

使用者問題：

```text
國外分公司退休員工的優待票規則是什麼？
```

讀取與處理：

- 讀取 `free_ticket_policy_index.md` 判斷路由。
- 讀取 `policy_retired_employee_tickets.md`。
- 原文只說國外各分公司退休（職）員工優待機票另依相關規定辦理。
- 不可自行推測國外分公司的細節。

回答範例：

```text
目前提供的規範內容只說明：國外各分公司退休（職）員工優待機票另依相關規定辦理。

目前沒有該「相關規定」的具體內容，因此不能直接判定國外分公司退休員工的具體適用方式。建議補充該規定文件，或洽人力資源部門確認。
```
