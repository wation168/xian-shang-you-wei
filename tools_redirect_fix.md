# /tools/ 404 轉址修復規格（給Claude Code）

## 背景
main.py（或對應路由層）當初工具頁改名時，只有 /patterns/ 有設301轉址，
/tools/ 這批漏了，導致舊網址變成真404。

## 需要新增的轉址對照表（確認需要的）
| 舊網址 slug | 新網址 slug |
|---|---|
| tax-bracket.html | income-tax.html |
| heloc-calculator.html | heloc-vs-personal-loan.html |
| protein-intake.html | protein-calculator.html |
| pension-calculator.html | pension-vs-lump-sum.html |
| roofing-calculator.html | roof-area.html |
| water-usage.html | water-intake.html |
| pet-insurance.html | pet-insurance-calc.html |

## 需要人工確認是否真下架（sitemap查無替代頁）
| 舊網址 slug | 語言 |
|---|---|
| self-employment-tax.html | de |
| sales-tax.html | zh-CN |
若確認真的下架，不設轉址，讓它自然404即可（不算bug）。

## 實作方式
比照 /patterns/ 現有轉址邏輯（main.py或nginx/Zeabur層應該已有一份轉址對照表，
先view確認現有實作方式，用同一套機制加規則，不要另開新邏輯）。
轉址規則需適用所有10語言資料夾，不是只修en版。

## 驗證方式
逐一 curl -I 每個舊網址（10語言 x 7個工具 = 70筆），確認都回301且Location
指向對應新網址，且新網址本身回200。
