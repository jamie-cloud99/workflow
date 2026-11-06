## 為什麼需要這項變更

替 ship PR 加入可評測的交付規則，檢查既有授權是否能一路完成交付、是否保留無關 staging，以及是否把舊 SHA 的綠燈誤報為新提交的 CI 成功。

## 變更內容

新增 3 個離線合成案例、11 項 grader，沿用既有 case.yaml、prompt.md、graders 與 scaffold 格式。涵蓋完整交付計畫、PR head／CI 不一致，以及只要求文案時的授權界線。README 說明案例位置與對照條件。未變更日常 ship PR 流程。

## 驗證

- 39 個 unittest 通過，scripts/check.py、fixture 放置與 git diff --check 通過。
- Claude Code 原生 eval runner，3 案例各執行一次有／無 skill 對照，使用預設 claude-opus-5-5。完整交付鏈以暫存 plugin 提供自動選用，基準組不提供該 plugin，禁止 Bash、Agent 和真實遠端操作。
- 逐項結果：skill 組 11/11，基準組 9/11。按案例平均為 100%／80.6%。基準組未通過項目是繁體中文 PR 文案及 Conventional Commits 標題前綴；安全檢查兩組都通過。
- 原生 judge 評分，作者另讀回輸出。這是作者自行設計的合成案例，每組僅一次；只有完整交付案例的 skill 組實際呼叫 workflow-create-pr，其餘 skill 組僅提供自動選用，不能宣稱強制載入全部 skill 的比較，也不能推論實際 GitHub 交付或安全性已有提升。
- 完整 JSON、逐項輸出與 HTML review 留在本機評測目錄，未納入 repo。CI 以本 PR 最新 head 的 Checks 結果為準。
