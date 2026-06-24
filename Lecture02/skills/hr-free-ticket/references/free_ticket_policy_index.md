# Free Ticket Policy Index 免費機票政策索引

本文件是 `hr-free-ticket` 的主要 routing index。處理免費機票、優待機票、ID00、ID00R1、ID00R2、點數、年資、眷屬、現職員工、退休（職）員工、外派依親、探親、效期與額度查詢時，先讀本文件，再依問題讀取精確 reference 或執行指定 script。

本文件只負責指引讀檔與工具使用，不作為政策細節依據。正式回答須依實際讀取的 policy reference 與 script 查詢結果組織。

## 使用原則

- 優先判斷使用者問題屬於「名詞定義」、「政策說明」、「ID00 點數查詢」、「優待機票額度查詢」或「多主題問題」。
- 政策說明讀取 `.md` policy reference。
- ID00 年資點數查詢必須執行 `scripts/lookup_employee_free_ticket_points_(ID00)table.py`。
- 優待機票額度查詢必須執行 `scripts/lookup_preferential_ticket_rules_summary_table.py`。若此 script 無法執行，不可直接讀取 JSON 表格人工判斷，應說明目前缺少可用查詢工具。
- `employee_free_ticket_points_(ID00)table.json` 與 `preferential_ticket_rules_summary_table.json` 只供 scripts 作為 source table，不是 agent 可直接讀取或人工解讀的 routing target。
- 使用者問題同時涉及政策與查表時，先取得查表結果，再讀取相關 policy reference 補充限制、效期或申請規則。
- 若 reference 只寫「另依相關規定」或「參照其他文件」，但該文件未收錄，不可自行推測。
- Routing 關鍵字應使用具情境的短語，不使用單一通用詞作為判斷依據。例如 F 艙、C 艙、W 艙、Y 艙、眷屬、配偶、父母、點數、退休、年資、效期等詞可能出現在多份文件，不能單獨決定路由。

## Routing Table

| Reference Key | 中文主題 | File / Tool | 使用者常見問法 / 關鍵字 | 適用情境 | 需同時讀取 / 執行 |
|---|---|---|---|---|---|
| `term_definitions` | 名詞定義 | `term_definitions.md` | ID00 是什麼、R1 及 R2 差異、CIZED 定義、進點日是什麼、OFF-LINE STATION 是什麼、DOJ 是什麼、TPM 是什麼、C / PY / W / Y 艙代表什麼 | 使用者明確詢問名詞、縮寫、票種、艙等代碼、身分定義，或英文 query 需要對應中文名詞時 | 視問題另讀對應 policy |
| `free_ticket_usage_ID00` | 免費機票 ID00 使用方式 | `policy_free_ticket_usage_ID00.md` | ID00 使用方式、ID00 基本點數計算、ID00 轉機可以從中停點搭嗎、ID00 可不可以先搭回程、ID00 孩童或嬰兒補稅、ID00 換搭航點、ID00 退稅、ID00 自助及網路報到 | 問 ID00 共通使用方式，包含基本點數規則、轉機、搭乘順序、補稅、換搭航點與報到限制 | 問名詞時讀 `term_definitions.md`；問詳細記點方式時讀 `china_airline_employee_free_ticket_point_usage_rules.md` |
| `free_ticket_point_usage_rules` | 華航員工免費機票點數使用方式規範 | `china_airline_employee_free_ticket_point_usage_rules.md` | ID00 詳細記點方式、華航員工免費機票點數使用方式規範、ID00 外部詳細記點、轉機航點詳細計點 | 只在問題涉及 `policy_free_ticket_usage_ID00.md` 指向的外部詳細記點規範，或該檔的基本點數規則不足以回答時使用 | 先讀 `policy_free_ticket_usage_ID00.md`；若本檔為空或未收錄所需細節，不可推測 |
| `free_air_tickets_for_current_employees_ID00` | 現職員工免費機票 ID00 | `policy_free_air_tickets_for_current_employees_ID00.md` | 現職員工 ID00 適用對象、現職員工 ID00 艙等、現職員工 ID00 配偶 / 眷屬可否使用、現職員工 ID00 點數效期、現職員工進點日、留停復職 ID00 進點日遞延、現職員工 ID00 人工開票效期 | 問現職員工 ID00 的適用艙等、對象、點數核予原則、點數效期、留停復職進點日遞延或機票效期 | 查年資點數時執行 `scripts/lookup_employee_free_ticket_points_(ID00)table.py`；問名詞時讀 `term_definitions.md` |
| `ticket_for_family_service_staff_ID00R2` | 家屬服務員 ID00R2 機票 | `policy_ticket_for_family_service_staff_ID00R2.md` | 家屬服務員 ID00R2、家屬服務員遴選、緊急應變人員 ID00R2、家屬服務員每年一次、家屬服務員單點來回、家屬服務員 ID00R2 可否改票或延長效期 | 問家屬服務員 ID00R2 的資格、核予方式、限制、是否可改票或延長效期 | 問 R2、空位搭乘或艙等時讀 `term_definitions.md` |
| `employee_recognition_award_ID00R1` | 員工楷模 ID00R1 機票 | `policy_employee_recognition_award_ID00R1.md` | 員工楷模 ID00R1、楷模票申請期限、當選楷模免費票、員工楷模本人與眷屬各一張、員工楷模父母年齡限制、員工楷模票可否改票或延長效期 | 問員工楷模 ID00R1 的適用對象、票數、申請期限、改票限制與效期 | 問艙等與對象時可讀 `policy_free_air_tickets_for_current_employees_ID00.md`；問名詞時讀 `term_definitions.md` |
| `dependent_relocation_ID00R1` | 眷屬依親 ID00R1 機票 | `policy_dependent_relocation_ID00R1.md` | 眷屬依親 ID00R1、外派依親票、奉派國外眷屬依親、輪調返國眷屬依親、外站調外站眷屬依親、人事通報一年內申請依親票、依親票 OFF-LINE STATION、依親票效期 | 問眷屬依親 ID00R1，包含外派、輪調返國、外站調派、申請時點、航點限制、OFF-LINE STATION 與效期 | 問 OFF-LINE STATION、ZED、眷屬或 R1 時讀 `term_definitions.md` |
| `dependent_home_visit_ID00R1` | 眷屬探親 ID00R1 機票 | `policy_dependent_home_visit_ID00R1.md` | 眷屬探親 ID00R1、外派探親票、進點日一年內申請探親票、探親票使用現有點數、探親票不可換搭同國其他航點、探親票 OFF-LINE STATION、探親票效期 | 問眷屬探親 ID00R1，包含每年進點日一年內申請、使用現有點數、航點限制、改票限制與效期 | 問 OFF-LINE STATION、ZED、眷屬、進點日或 R1 時讀 `term_definitions.md` |
| `retired_employee_tickets` | 退休（職）員工機票 | `policy_retired_employee_tickets.md` | 退休後還有 ID00 嗎、退休（職）員工 ID00、退休員工 ID00 艙等、退休後次年度點數、退休當年度未用點數、退休前後開票排序、服務滿 20 年退休 ID00R1、退休後有價優待票、退休員工線上登入、國外分公司退休員工優待票 | 問退休（職）員工 ID00、艙等、核予年限、退休當年度與次年度點數、開票排序、滿 20 年 ID00R1、有價優待票、線上申請方式或效期 | 問有價優待票額度時執行 `scripts/lookup_preferential_ticket_rules_summary_table.py`；問名詞時讀 `term_definitions.md` |
| `employee_free_ticket_points_lookup` | ID00 年資點數查詢 | `scripts/lookup_employee_free_ticket_points_(ID00)table.py` | 年資 X 年 ID00 有幾點、現職員工年資 X 年 ID00 點數、ID00 原優待機票點數、ID00 調整配點、ID00 points by seniority | 使用者提供或詢問現職員工 ID00 年資點數時 | 必須執行 script；不可直接讀取或人工解讀 `employee_free_ticket_points_(ID00)table.json`；通常同時讀 `policy_free_air_tickets_for_current_employees_ID00.md` |
| `preferential_ticket_quota_lookup` | 優待機票額度查詢 | `scripts/lookup_preferential_ticket_rules_summary_table.py` | 現職員工 ID75 額度、退休員工 ID90 額度、滿 25 歲以上子女 ID75 幾次、未滿 25 歲子女 CIZED 額度、配偶 ID50 幾次、父母 ID90 幾次、有價優待票額度查詢 | 使用者問某身分、票種、艙等、員工狀態、年資月數可用額度時 | 必須執行 script；若缺員工狀態、身分分組、票種、艙等或年資月數，先追問；不可直接讀取或人工解讀 `preferential_ticket_rules_summary_table.json` |
| `response_examples` | 回答範例 | `response_examples.md` | 回答範例、測試案例、如何回答 ID00 點數、如何回答退休票、如何回答缺少外部規範 | 只在需要參考 routing 或回答組織方式時使用 | 不作為政策依據 |

## 常見組合

| 問題類型 | 讀取 / 執行順序 |
|---|---|
| 問 ID00 使用方式、轉機、換搭、補稅 | 讀 `policy_free_ticket_usage_ID00.md`；必要時讀 `term_definitions.md`。 |
| 問 ID00 詳細記點方式 | 先讀 `policy_free_ticket_usage_ID00.md`，再讀 `china_airline_employee_free_ticket_point_usage_rules.md`；若外部詳細規範未收錄，不可推測。 |
| 問現職員工 ID00 艙等或點數效期 | 讀 `policy_free_air_tickets_for_current_employees_ID00.md`；必要時讀 `term_definitions.md`。 |
| 問年資 X 年有多少 ID00 點數 | 讀 `policy_free_air_tickets_for_current_employees_ID00.md`，執行 `scripts/lookup_employee_free_ticket_points_(ID00)table.py`。 |
| 問退休後 ID00 或退休排序 | 讀 `policy_retired_employee_tickets.md`。 |
| 問退休後有價優待票額度 | 讀 `policy_retired_employee_tickets.md`，再執行 `scripts/lookup_preferential_ticket_rules_summary_table.py`；若 script 無法執行，不可直接讀 JSON。 |
| 比較依親票與探親票 | 同時讀 `policy_dependent_relocation_ID00R1.md` 與 `policy_dependent_home_visit_ID00R1.md`。 |
| 問 ID00R1 / ID00R2 差異 | 讀 `term_definitions.md`，再依情境讀 `policy_employee_recognition_award_ID00R1.md`、`policy_dependent_relocation_ID00R1.md`、`policy_dependent_home_visit_ID00R1.md` 或 `policy_ticket_for_family_service_staff_ID00R2.md`。 |
| 問未收錄之外部規定 | 讀到相關 policy 後，若只寫另依相關規定辦理，回答目前提供的規範內容未收錄細節，不可推測。 |

## 缺少資訊時先追問

查詢優待機票額度前，若缺少以下必要資訊，先追問，不要自行假設：

- 員工狀態：現職員工或退休（職）員工。
- 身分分組：員工本人、配偶、父母、未滿 25 歲子女、滿 25 歲以上子女、眷屬、Travel Mate 等。
- 票種或折扣別：ID00、ID00R1、ID00R2、ID90、ID75、ID50、CIZED、ZED。
- 艙等：F、C、W / PY、Y。
- 年資單位與數值：年資年數或年資月數。
- 情境：現職、退休、家屬服務員、員工楷模、眷屬依親、眷屬探親。

## 禁止推測

- 不可把 ID00、ID00R1、ID00R2 視為相同規則。
- 不可把現職員工與退休（職）員工規則混用。
- 不可把眷屬依親與眷屬探親規則混用。
- 不可直接讀取或人工解讀兩個 JSON table 產生答案。
- 不可用 `response_examples.md` 當作政策依據。
- 不可自行補充「華航員工免費機票點數使用方式規範」、家屬服務員遴選外部規定、有價機票效期、國外分公司退休（職）員工規定或聯航 ZED 細節等未收錄內容。
