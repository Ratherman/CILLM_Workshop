# 假別政策索引

回答請假政策問題前，先使用本索引判斷應讀取哪一個政策檔案。實際檔名請以表格中的 `Policy File` 欄位為準。

政策檔案內容以中文撰寫，最終回答也應使用中文。本索引保留中文常見問法、同義詞與容易混淆的判斷提示，讓 agent LLM 能從使用者的中文問題找到正確政策檔案。

## 工作時間、例假和休息日、國定及民俗假日索引

 - 下列情境不是單一假別政策，但會影響請假、排班、工作日或假日判斷。若使用者問題涉及以下任一情境，需同時讀取 `general_attendance_and_holiday_rules.md`，不可只讀單一假別政策檔案。

| Reference Key | 中文 | Policy File | 使用者常見問法 / 關鍵字 | 適用情境 |
|---|---|---|---|---|
| `general_attendance_and_holiday_rules` | 工作時間、例假和休息日、國定及民俗假日 | `general_attendance_and_holiday_rules.md` | 工作時間、工時、全年工時、每週工時、例假、休息日、國定假日、民俗假日、工作日調移、休假日調移、休息日上班、例假上班、地勤正班/輪班排班、空勤請休假 | 問工時、例假與休息日、國定及民俗假日、連續工作日、工作日調移、地勤正班/輪班排班、休息日或例假出勤、空勤請休假等規則。 |

### 讀取原則

- 問題同時涉及假別政策與例假、休息日、國定假日、連續工作六日、工作日調移或排班，需同時讀取 `Policy File` 欄位指定的政策檔案與 `general_attendance_and_holiday_rules.md`。
- 若問題只涉及工時、例假、休息日、國定及民俗假日、連續工作日、工作日調移或排班，直接讀取 `general_attendance_and_holiday_rules.md`。
- 若使用者詢問空勤員工請休假，本 SKILL 未收錄 OG-021 或 EZ-013 原文，只能告知其依此兩份品質文件辦理，不可自行推測空勤請休假細節。

## 一般假別對照表

| Reference Key | 中文假別 | Policy File | 使用者常見問法 / 關鍵字 | 適用情境 | 需同時讀取 |
|---|---|---|---|---|---|
| `annual_paid_leave` | 特別休假 | `policy_annual_paid_leave.md` | 特休、特別休假、年假、休假、年資給假、未休、折發工資、補休、特休排休、離職特休結清 | 問年資給假日數、特休排休、特休計算單位、未休折發、離退特休處理、加班補休與特休結清。 |  |
| `business_trip_leave` | 公差 | `policy_business_trip_leave.md` | 公差、出差、差旅、派遣外地、國外公差 | 問簽奉核准至外地執行業務，且適用差旅費報支規定的請假與補休規則。 |  |
| `official_outing_leave` | 公出 | `policy_official_outing_leave.md` | 公出、外出洽公、臨時公出、出席公司舉辦活動 | 問主管指派離開日常辦公處所執行的業務，且不適用差旅費報支規定的情境。 |  |
| `public_duty_leave` | 公假 | `policy_public_duty_leave.md` | 公假、兵役召集、政府召集、選舉、法院作證、防疫、政府活動 | 問政府召集、兵役、選舉、法院刑事庭作證、防疫或奉派參加機關團體活動等公假。 |  |
| `union_meeting_leave` | 會務假 | `policy_union_meeting_leave.md` | 會務假、工會、工會法、團體協約規定、工會會議 | 問依工會法或公司團體協約辦理的工會會務假。 |  |
| `occupational_injury_or_illness_leave` | 公傷病假 | `policy_occupational_injury_or_illness_leave.md` | 公傷病假、職災、職業災害、公傷、職業傷害、職業疾病 | 問因職業災害導致失能、傷害或疾病時的治療、休養、證明、請假上限與審查規則。 |  |
| `sick_leave` | 未住院／住院傷病假（病假） | `policy_sick_leave.md` | 病假、傷病假、未住院病假、住院病假、普通傷害、疾病、連續病假、病停、留職停薪、病假工資 | 問一般疾病或普通傷害治療休養、未住院或住院病假、病假日數、工資、證明文件、超假或病停。 |  |
| `cancer_sick_leave` | 癌症病假 | `policy_cancer_sick_leave.md` | 癌症病假、癌症、原位癌、癌症門診、癌症治療、癌症傷病假、癌症病假工資 | 問罹患癌症或原位癌並採門診方式治療時，使用傷病假額度的特殊規則。 | `sick_leave` |
| `pregnancy_rest_leave` | 安胎假 | `policy_pregnancy_rest_leave.md` | 安胎假、安胎、懷孕休養、孕期休養、婦產科證明、安胎日數、安胎假中流產、安胎假中分娩 | 問懷孕期間經醫師診斷需安胎休養時，使用傷病假額度的特殊規則。 | `sick_leave` |
| `menstrual_leave` | 生理假 | `policy_menstrual_leave.md` | 生理假、生理期、月經、生理原因、生理假工資 | 問因生理原因必須治療或休養的生理假、與未住院傷病假的合計、工資或不得不利處分。 | `sick_leave` |
| `marriage_leave` | 婚假 | `policy_marriage_leave.md` | 婚假、結婚、結婚登記 | 問員工結婚請假、婚假日數、婚假證明文件、結婚登記日前後請假或婚假逾期補件。 |  |
| `maternity_leave` | 產假 | `policy_maternity_leave.md` | 產假、分娩、流產、產假工資、產假日數 | 問員工分娩前後或流產時的產假、日數、證明、工資與計假規則。 |  |
| `prenatal_checkup_leave` | 產檢假 | `policy_prenatal_checkup_leave.md`  | 產檢假、產檢 | 問員工懷孕期間請產檢假時所需證明及計假方式。 |  |
| `paternity_and_prenatal_checkup_leave` | 陪產檢及陪產假 | `policy_paternity_and_prenatal_checkup_leave.md` | 陪產檢假、配偶妊娠、配偶懷孕、配偶分娩、配偶生產、國內外派員工陪產 | 問員工配偶妊娠期間產檢及生產前後相關請假規範，並包含陪產期間規則。 |  |
| `personal_leave` | 事假 | `policy_personal_leave.md` | 事假、事故、親自處理、家庭照顧假、照顧家人、事假超過、特休抵充 | 問員工因個人事故必須親自處理、一般事假、家庭照顧假、事假日數、事假工資或超過日數處理。 |  |
| `parental_personal_leave` | 育嬰事假 | `policy_parental_personal_leave.md` | 育嬰事假、育嬰、未滿三歲子女照顧、撫育子女 | 問地勤人員為撫育未滿三歲子女申請育嬰事假。 |  |
| `bereavement_leave` | 喪假 | `policy_bereavement_leave.md` | 喪假、奔喪、親屬喪亡 | 問親屬喪亡時依親等核給喪假日數、證明文件、外派路程假或返國奔喪規則。 |  |
| `indigenous_ceremony_leave` | 原住民歲時祭儀假 | `policy_indigenous_ceremony_leave.md` | 原住民歲時祭儀假、歲時祭儀假、歲時祭儀日 | 問原住民歲時祭儀期間的請假規則、計假方式及工資發給規則。 |  |

## 選檔原則

- 回答前必須要讀取選中的政策檔案，不要只根據本索引回答。
- 若使用者詢問證明文件、給假日數、計假方式、工資、累積起止日、請假限期、超假處理或其他額外規定，需讀取相關政策檔案，並依政策檔案內容用中文回答，且引用內容回答時以政策檔案內的原文為主。
- 若同一個問題可能涉及多個假別，讀取所有可能相關的政策檔案，並在回答中並列陳述每個假別的政策說明，不可以融合政策回答。
- 若問題是核決權限，先用本索引判斷假別，再讀取 `approval_authority_rules.md`。

## 病假相關特殊規則

- 若使用者提問請假相關問題時，提到癌症、原位癌、癌症門診或癌症治療，需同時讀取 `sick_leave` 與 `cancer_sick_leave`。
- 若使用者提問請假相關問題時，提到安胎、懷孕休養、孕期休養或孕期需休養，需同時讀取 `sick_leave` 與 `pregnancy_rest_leave`。
- 若使用者提問請假相關問題時，提到 生理假、生理期、月經或月經不適，需同時讀取 `sick_leave` 與 `menstrual_leave`。
- 回答癌症病假、安胎假、生理假時，需同時說明其與一般病假的關係，以及特殊假別自己的證明文件、給假日數、計假方式、工資、限制與額外規定。

## 常見混淆判斷

- 公差涉及簽奉核准至外地執行業務，且適用差旅費報支規定。使用 `business_trip_leave`。
- 公出是主管指派離開日常辦公處所執行業務，且不適用差旅費報支規定。使用 `official_outing_leave`。
- 公假涉及政府召集、兵役召集、選舉、法院作證、防疫或奉派參加外部機關團體活動。使用 `public_duty_leave`。
- 事假是一般個人私事或事故請假，使用 `personal_leave`。育嬰事假是撫育未滿三歲子女的獨立假別，不占用一般事假。若使用者提到育嬰、照顧未滿三歲子女，使用 `parental_personal_leave`。
- `policy_prenatal_checkup_leave.md` 與 `policy_paternity_and_prenatal_checkup_leave.md` 的檔名和內容接近。依「適用情境」判斷：配偶妊娠、陪產檢、陪產問題使用 `paternity_and_prenatal_checkup_leave`。員工本人懷孕產檢或妊娠期間請假使用 `prenatal_checkup_leave`。
