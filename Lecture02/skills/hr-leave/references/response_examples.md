# Response Examples 回答範例

本文件只提供回答格式與路由判斷範例，不是政策依據。回答任何請假政策問題時，仍必須先讀取 `leave_policy_index.md` 及相關 reference 或政策檔案，不可只根據本文件回答。

## 使用規範

 - 本文件用於提供 reference 讀取順序、路由判斷，以及回答組織方式範例。
 - 本文件不是政策依據，不可把本文件當成政策原文。
 - 若範例或本文件內容與政策檔案內容不同，以政策檔案為準。
 - 使用者問題涉及未收錄文件，明確告知使用者該文件或內容未收錄，不可自行推測或創造規範。
 - 若問題提到某假別，但實際詢問核心是例假、休息日、國定假日、連續工作日、工作日調移或排班，優先讀取 `general_attendance_and_holiday_rules.md`。只有使用者同時詢問該假別本身的給假、證明、工資、排休、額度或超假處理時，才讀取該假別政策檔案。

## 單一對話範例

### 範例 1 : 單一假別詢問

#### User query

事假一年最多可以請幾天?

#### References To Load

1. `leave_policy_index.md`
2. `policy_personal_leave.md`

#### Response Pattern

1. 先說明使用者問題適用假別為「事假」。
2. 根據 `policy_personal_leave.md` 回答給假日數。
3. 如問題涉及工資、超假或證明文件，再補充對應規定。
4. 不要引用其他假別規則。

#### Response Skeleton

詢問的是「事假」規定。依事假政策，事假的給假日數為：

- 給假日數：依 `policy_personal_leave.md` 的「給假日數」欄位回答。
- 計假方式：如使用者有問，再依政策檔補充。
- 工資：如使用者有問，再依政策檔補充。

如果請假日數超過規定，需依政策檔中的超假處理方式辦理。

### 範例 2 : 特殊傷病假問題

#### User Query

我懷孕想要請安胎假，這算不算病假?需要附上哪些證明?

#### References To Load

1. `leave_policy_index.md`
2. `policy_pregnancy_rest_leave.md`
3. `policy_sick_leave.md`

#### Response Pattern

1. 先判斷此問題涉及「安胎假」。
2. 讀取 `policy_pregnancy_rest_leave.md` 用以說明安胎假與一般傷病假的關係。
3. 根據 `policy_pregnancy_rest_leave.md` 回答安胎假的證明文件、給假日數、計假方式與限制。
4. 如涉及病假額度或工資，再同時參考 `policy_sick_leave.md`。
5. 不可只根據一般病假回答安胎假的證明文件或特殊規則。

#### Response Skeleton

詢問的是「安胎假」規定。因為問題也提到是否算病假，需同時說明安胎假與傷病假的關係。

依 `policy_pregnancy_rest_leave.md`：

- 與傷病假的關係：依政策檔「請假條件」或相關欄位回答。
- 所需證明：依政策檔「所需證明」欄位回答。
- 給假日數：依政策檔「給假日數」欄位回答。
- 計假方式：依政策檔「計假方式」欄位回答。

若問題涉及病假額度或工資，再依 `policy_sick_leave.md` 補充傷病假額度或工資發給方式。

### 範例 3 : 提到多種假別規範但實際核心僅為一種假別

#### User Query

我排特休可以中斷連續工作六日嗎？

#### References To Load

1. `leave_policy_index.md`
2. `general_attendance_and_holiday_rules.md`

#### Response Pattern

1. 先判斷問題核心是「連續工作日是否中斷」，不是特別休假的給假、排休或工資。
2. 雖然使用者提到特休，但若未詢問特休給假日數、排休、工資、未休折發或特休額度，不需讀取 `policy_annual_paid_leave.md`。
3. 「連續工作日是否中斷」，依 `general_attendance_and_holiday_rules.md` 回答。
4. 不要延伸回答特休政策細節除非使用者詢問特休給假、排休或工資發給。

#### Response Skeleton

詢問的是「特休是否可中斷連續工作六日」。這題的核心是連續工作日中斷規則，屬於共通差勤規則，不是特休給假、排休或工資問題。

依 `general_attendance_and_holiday_rules.md`：

- 連續工作日中斷規則：依政策檔中「其他規定及說明」或相關欄位回答。
- 是否需要讀取特休政策：若使用者未詢問特休給假日數、排休、工資、未休折發或特休額度，不需延伸回答特休政策。

若使用者後續追問特休給假、排休或工資發給，再讀取 `policy_annual_paid_leave.md` 補充。

### 範例 4 : 請假准假權責問題

#### User Query

一般員工請 8 天喪假需要誰核准?

#### References To Load

1. `leave_policy_index.md`
2. `approval_authority_rules.md`

#### Response Pattern

1. 問題提到喪假但實際是在問「核准」問題，不是喪假的給假條件、日數或工資問題，因此不需要讀取 `policy_bereavement_leave.md`。
2. 若使用者同時詢問喪假日數、證明或工資，才讀取 `policy_bereavement_leave.md`。
3. 讀取 `approval_authority_rules.md` 並確認喪假在 `approval_authority_rules.md` 中屬於哪一組。
4. 依請假人員職務與請假日數找到對應准假權責。
5. 若使用者未提供職務或日數，應請使用者補充，不可猜測。
6. 准假主管依 `approval_authority_rules.md` 中表格回答。

#### Response Skeleton

你詢問的是「喪假 8 天的准假權責」。這題的核心是核准權責，不是喪假的給假條件、日數或工資。

依 `approval_authority_rules.md`：

- 適用假別分組：依政策檔中喪假所屬分組回答。
- 請假人員職務：依使用者提供的職務判斷。
- 請假日數：依使用者提供的 8 天判斷。
- 准假主管：依政策檔表格中對應職務與日數區間回答。

若使用者同時詢問喪假的日數、證明文件或工資，再讀取 `policy_bereavement_leave.md` 補充。

### 範例 5 : 未收錄外部文件

#### User Query

空勤員工想請休假該怎麼請？

#### References To Load

1. `leave_policy_index.md`
2. `general_attendance_and_holiday_rules.md`

#### Response Pattern

1. 判斷問題涉及空勤員工請休假。
2. 讀取 `general_attendance_and_holiday_rules.md`。
3. 若本 skill 未收錄 OG-021 或 EZ-013 原文，只能告知依該文件辦理。
4. 不可自行推測空勤請休假細節。

#### Response Skeleton

你詢問的是「空勤員工請休假」規定。

依 `general_attendance_and_holiday_rules.md`：

- 適用文件：依政策檔中空勤員工請休假的外部文件名稱回答。
- 本 skill 收錄限制：若本 skill 未收錄外部文件原文，需明確告知目前無法依該外部文件回答細節。

目前本 skill 未收錄相關外部文件完整內容時，不可自行推測空勤請休假的申請方式、給假日數、工資或其他細節。

## 多輪對話範例

### 多輪對話原則

- 只有在缺少必要判斷資訊時才追問。
- 追問時只問必要資訊，避免要求使用者提供過多資料。
- 使用者補充資訊後須結合前一輪的 user query 再開始判讀。
- 使用者補充資訊後，需重新判斷應讀取哪些 reference。
- 不可在資訊不足時自行假設職務、假別、請假日數、到職日、員工類型或住院與否。

### 範例 1 : 詢問核決權限時資訊不足

#### User Query

我請假 3 天要誰核准？

#### References To Load

1. `leave_policy_index.md`

#### Response Pattern

1. 判斷此問題屬於准假權責。
2. 發現缺少假別與請假人員職務。
3. 不可自行推測准假主管。
4. 先請使用者補充假別與職務。

#### Multi-turn Skeleton

User: 我請假 3 天要誰核准？

Assistant: 需要先確認兩項資訊，才能判斷准假權責：

1. 你要請的是哪一種假別？
2. 你的職務或層級是什麼？

請提供後，我會依准假權責規則判斷。

User: 我是一般員工，要請事假。

#### References To Load After User Reply

1. `leave_policy_index.md`
2. `approval_authority_rules.md`

#### Final Response Pattern

1. 判斷問題為詢問准假權責，假別為事假。
2. 依 `approval_authority_rules.md` 找出事假所屬組別。
3. 依 `approval_authority_rules.md` 中表格，一般員工與 3 日區間回答准假權責。

### 範例 2 : 詢問特休給假時年資資訊不足

#### User Query

我今年有幾天特休？

#### References To Load

依下列順序讀取：

1. `leave_policy_index.md`
2. `policy_annual_paid_leave.md`

#### Response Pattern

1. 判斷問題涉及特別休假。
2. 發現缺少年資或到職日。
3. 不可自行推測特休日數。
4. 請使用者補充目前年資。

#### Multi-turn Skeleton

User: 我今年有幾天特休？

Assistant: 請提供你的目前服務年資，才能依特休政策判斷給假日數。

User: 我目前年資 3 年。

#### References To Load After User Reply

1. `leave_policy_index.md`
2. `policy_annual_paid_leave.md`

#### Final Response Pattern

1. 根據使用者提供的服務年資查詢 `policy_annual_paid_leave.md`。
2. 依 `policy_annual_paid_leave.md` 的年資給假表回答。
3. 若涉及特休年度或結算給假日，再補充相關規則。

### 範例 3 : 員工類型資訊不足

#### User Query

國定假日不能休的話可以補休嗎？

#### References To Load

1. `leave_policy_index.md`
2. `general_attendance_and_holiday_rules.md`

#### Response Pattern

1. 判斷問題涉及國定及民俗假日與排班。
2. 若回答需要區分地勤正班、地勤輪班或空勤員工，但使用者未提供員工類型，需要求提供。
3. 不可自行假設使用者是地勤或空勤。
4. 若本 skill 未收錄外部文件內容，不可推測外部文件規定，應該告知使用者自行查詢該文件或聯絡人力資源部門。

#### Multi-turn Skeleton

User: 國定假日不能休的話可以補休嗎？

Assistant:
這題會因員工類型與排班方式不同而影響判斷。請先確認您是哪一類：

1. 地勤正班人員
2. 地勤輪班人員
3. 空勤員工

User: 我是地勤輪班人員。

#### References To Load After User Reply

1. `leave_policy_index.md`
2. `general_attendance_and_holiday_rules.md`

#### Final Response Pattern

1. 依 `general_attendance_and_holiday_rules.md` 回答輪班員工因排班無法於國定及民俗假日休假時的處理方向。
2. 若文件只指向其他公司規定，明確告知需依該文件辦理。
3. 不可自行推測加班費、誤餐夜點費或補休細節。
