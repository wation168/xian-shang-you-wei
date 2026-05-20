# Claude Code 設定

## 權限
- 所有工具操作直接執行，不需要逐一確認
- 允許讀寫專案內所有檔案
- 允許執行 Python、PowerShell、bash 指令
- 允許讀取 C:\Windows\Fonts\

## 操作原則
- 啟動時讀取 總結.md 取得專案上下文
- 只讀取需要修改的相關檔案，不要整份讀取
- 修改完列出改動摘要
- 大改動前確認 git 有 commit
