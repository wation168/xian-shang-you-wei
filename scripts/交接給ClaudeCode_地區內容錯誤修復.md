# 任務交接：全站工具頁「地區內容跟語言不符」錯誤修復

## 所需檔案位置一覽（全部列在這，不用自己找）

| 東西 | 路徑 |
|---|---|
| 這份任務說明文件本身 | `D:\xian-shang-you-wei\scripts\交接給ClaudeCode_地區內容錯誤修復.md` |
| 掃描腳本 | `D:\xian-shang-you-wei\scripts\scan_locale_mismatch.py` |
| 掃描目標根目錄（全部工具頁都在這底下） | `D:\xian-shang-you-wei\backend\frontend\tools\` |
| 掃描完會產出的報告（腳本自動產生，不用手動建立） | `D:\xian-shang-you-wei\scripts\locale_mismatch_report.csv` |
| 已確認bug①：rental-yield 繁中版 | `D:\xian-shang-you-wei\backend\frontend\tools\rental-yield.html` |
| 已確認bug①：rental-yield 德文版 | `D:\xian-shang-you-wei\backend\frontend\tools\de\rental-yield.html` |
| 已確認bug②：salary-raise 西班牙文版 | `D:\xian-shang-you-wei\backend\frontend\tools\es\salary-raise.html` |
| 已確認bug③：court-fee 繁中版（最急） | `D:\xian-shang-you-wei\backend\frontend\tools\court-fee.html` |
| 已修好可對照的範例（同類型bug的修復參考範本） | `D:\xian-shang-you-wei\backend\frontend\tools\es\life-insurance-calc.html` |
| 完成後的總結文件要放哪 | 存成 `D:\xian-shang-you-wei\scripts\本次任務完成總結.md`（沿用之前的檔名習慣），並提醒使用者上傳到 Project 檔案區 |

各語言資料夾對應規則：繁中在 `tools\` 根目錄（無子資料夾），其他語言各自
`tools\{語言代碼}\`，例如 `tools\es\`、`tools\de\`、`tools\ja\`、`tools\ko\`、
`tools\fr\`、`tools\pt\`、`tools\id\`、`tools\zh-CN\`、`tools\en\`。

## 背景

`es/life-insurance-calc.html`（西班牙文版）被發現內文寫「在英國」「英鎊」「英國保險公司」，
但頁面是西班牙文版、幣別符號用€。判斷是拿UK模板產生其他語言版本時，翻譯了文字，
但沒把「英國」相關的地區內容一併改掉，留下了英國的痕跡。這份文件已經修好並部署。

現在要用同樣的邏輯，掃描全站 `backend/frontend/tools/` 底下所有語言版本，找出同類型錯誤並修正。

## 附帶的掃描腳本

`scan_locale_mismatch.py` 已經放在 `D:\xian-shang-you-wei\scripts\` 底下
（跟其他既有腳本同一個資料夾，不要放進 `backend\`，避免被誤上傳部署）。

在該資料夾底下直接執行：

```
cd D:\xian-shang-you-wei\scripts
python scan_locale_mismatch.py
```

預設掃描 `D:\xian-shang-you-wei\backend\frontend\tools\`，會產出 `locale_mismatch_report.csv`。

**這支腳本的 A 類檢查（locale字串不符）已知會產生大量誤判**，因為全站JS數字格式
本來就統一寫死用 `en-US`/`en-GB`，不分頁面語言，這是既有的技術設計，不是bug，
**A類結果可以直接忽略**，不用處理。

**只看 B 類（關鍵字疑似誤植）**，但B類同樣需要人工/AI判斷過濾，因為很多工具
本來就該提到英國（見下方誤判排除清單）。

## 已確認的誤判排除清單（這些工具提到英國是正常的，不要動）

這幾個工具因為其技術本質就是英國相關內容，掃描抓到「英國」「£」是**正常且正確**的，
**不要修改**：

- `payroll-tax.html` `bonus-tax.html` `stamp-duty.html` `take-home-pay.html`
  —— 本來就是英國稅制專用工具（已由使用者確認）
- `clothing-size.html` `ring-size-converter.html` `shoe-size-converter.html`
  —— 尺碼對照表，本來就要列英制系統做比較
- `oven-converter.html` —— Gas Mark是真實的英國烤箱刻度標準
- `wire-gauge.html` `engine-horsepower.html` `fuel-efficiency.html`
  —— 真實的英制技術標準（線規、馬力、英制加侖MPG），跟其他制度比較是正常內容
- `toefl-ielts.html` `ielts-band.html` —— IELTS真的是英國文化協會主辦，提到英國是事實
- `vat-calculator.html` `currency-converter.html`
  —— 多國稅率/幣別對照表，英國只是列舉的其中一項，不是唯一基準

如果掃描發現以上清單「以外」的工具也把英國當成「多國比較中的一項」（例如列舉
「美國X%、英國Y%、日本Z%」這種對照表），也算正常，不用改。

**注意：英文版（`tools\en\`）目前不在這次掃描範圍內**（`scan_locale_mismatch.py`
裡英文語言的關鍵字清單是空的），因為無法判斷英文版的「基準受眾」是哪個地區，
這部分先不處理，除非之後使用者另外指示。

## 判斷是否為真bug的準則

**真bug的特徵**：把「英國」的數據/規則當成**唯一基準**講，而不是列舉比較中的一項。
例如：
- ❌「在英國，加薪幅度通常是2-4%」（單一國家當成通用基準，這是bug）
- ✅「美國平均加薪3%，英國4%，日本2%」（列舉比較，這是正常內容）

## 已確認的3個真bug（優先處理）

| 檔案 | 語言 | 問題 |
|---|---|---|
| `rental-yield.html` | 繁中 (`tools\rental-yield.html`) | 「英國的平均租賃收益率通常在4%至8%」當成唯一標準講，沒有比較 |
| `rental-yield.html` | 德文 (`tools\de\rental-yield.html`) | 同上，「Im Vereinigten Königreich gelten Renditen zwischen 5%...」 |
| `salary-raise.html` | 西班牙文 (`tools\es\salary-raise.html`) | 「El aumento promedio en el Reino Unido...」把英國加薪幅度當成唯一基準 |
| `court-fee.html` | 繁中 (`tools\court-fee.html`) | **最急**——文字直接宣稱「根據英國法院官方費率計算」，如果這工具是給其他地區用的，代表可能連計算公式的基準都是錯的，不只是文字問題，需要額外確認 `calculate()` 函式裡的費率數字/級距是否真的是英國制度，如果是，要嘛整頁改成明確標示「英國法院費用估算」，要嘛要重新設計成通用/在地化版本 |

**這3個只是抽樣抓到的**，`rental-yield.html` 跟 `court-fee.html` 應該還有其他語言版本
（總共9個非英文語言）也需要檢查是否中獎，掃描腳本+人工判斷準則跑一次全部語言版本。

## 規模參考（讓你估工作量用）

這次掃描B類（關鍵字疑似誤植）總共抓到948筆、涉及221個不同檔案、75種不同工具名稱。
扣掉上面誤判排除清單那14種工具（占了大部分筆數），實際需要人工判斷的工具數量會少很多，
但仍然有一批完全沒被分類過的工具（例如 `gsm-converter.html` `yarn-weight.html`
`appliance-energy.html` 等等），這些**還沒被判斷過是真bug還是誤判**，需要照上面的
「判斷準則」重新過一次，不能假設除了列出的3個以外就沒有其他真bug了。

## 修復方式（比照 life-insurance-calc.html 的做法）

1. 把「唯一基準式」的英國文字，改成不特定國家、不編造假數字的通用敘述
   （例如「英國平均租賃收益率4-8%」→「市場平均租賃收益率通常落在4-8%之間，實際數字依地區而異」）
2. 如果原本的數字本身是真實可信的參考範圍，可以保留數字但拿掉「英國」的歸屬，
   當作通用示意範圍即可，不需要編造新數字
3. 檢查同一個檔案裡的JS數字格式（`toLocaleString(...)`），如果用了跟頁面語言明顯不符
   的locale（例如日文頁用`en-GB`），可以順手改成該語言對應的正確locale碼，
   但這不是強制的，優先度低於文字內容修正
4. 修完用文字比對/正則確認沒有殘留「Reino Unido」「británic」「Vereinigtes Königreich」
   「britannique」「英國」「영국」「イギリス」等對應語言的錯誤字樣
5. 確認HTML結構沒被破壞（h1/h2數量、article/table開閉標籤數量、行數大致合理）
6. **檔案編碼/換行符號**：這些html檔案是UTF-8、CRLF（\r\n）換行，用bytes層級
   （`rb`/`wb`）或確保編輯器不會偷偷轉成LF，main.py之前多次因為文字模式讀寫
   把CRLF轉成LF吃過虧，html檔案也要比照小心
7. **這次規模較大（可能涉及數十個檔案），照使用者的硬規則**：改之前先列出「哪些檔案、
   改什麼、為什麼」給使用者確認，不要一次全部改完才報告；建議先處理3個已確認的真bug
   並回報，確認做法沒問題後，再繼續處理剩餘未分類的工具

## 完成後：一定要產出完成總結文件

存成 `D:\xian-shang-you-wei\scripts\本次任務完成總結.md`，格式比照上次的
`本次任務完成總結.md`（表格列出：改了哪個檔案、改了什麼、重點說明），至少要包含：

1. **這次總共掃了幾個檔案、B類抓到幾筆、扣掉誤判排除清單後實際需要判斷的有幾筆**
2. **逐一列出每個判定為「真bug」的檔案**：檔案路徑、原本錯誤的文字、改成什麼
3. **逐一列出每個判定為「誤判、不用改」的工具**（除了文件裡已經列的14種之外，
   如果又新判斷出其他誤判案例，也要列出來、附上為什麼判斷是誤判的理由，
   這樣使用者可以檢查判斷邏輯對不對，不是自己猜的黑盒子）
4. **「順便留意，但不要順便修」那節記錄到的其他bug清單**（檔案名稱+一句話描述）
5. **驗證方式**：怎麼確認修完沒有殘留錯誤字樣、HTML結構沒壞掉
6. **還沒處理完的部分**：如果這次沒能一次掃完全部語言版本或全部工具，要清楚寫
   還剩下什麼沒做，不要讓使用者誤以為全部都處理完了

這份總結是要給下一個接手的Claude（可能是我，也可能是別的對話）快速核對用的，
寫得越具體、可查核，之後接手的人越不用重新摸索一次。

## 順便留意，但不要順便修

修這批地區內容錯誤時，會逐一打開每個中獎檔案，這時候如果**順便**發現其他明顯問題
（例如：
- 資料寫死過時年份，像2024/2025稅率/門檻沒更新
- JS計算邏輯明顯有bug（例如公式算出負數、除以零、變數名稱打錯）
- 內部連結指到不存在的頁面
- 其他跟「地區內容不符」無關的異常

**只需要記下來（檔案名稱+問題一句話描述），列進最後的完成總結裡，不要當場修**。
這是為了避免任務範圍不斷擴大、原本這批地區內容錯誤反而修不完。有了這份清單，
使用者可以之後再開新任務逐一處理，不用现在一次做完。
