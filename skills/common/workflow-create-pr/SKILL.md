---
name: workflow-create-pr
description: 使用者要求建立或更新 GitHub PR、開 pull request，或完成已授權的 ship PR 流程時使用；PR review 使用 workflow-review。
---

# workflow-create-pr

把已授權的變更交付成可 review 的 PR，確認遠端內容、分支關係與實際 CI 狀態。

## 準備與範圍

1. 讀取 repo 的 PR 規範與 template，確認任務、Git 狀態、head branch、base branch、remote 與 GitHub 身分。base 依使用者指定、分支依賴或 repo 規範決定；多帳號沿用對應 SSH／CLI 身分，避免改動無關的全域設定。
2. 查看 base 到 head 的 commits 與 diff，確認只包含本次交付。仍需提交的本次變更先使用 [workflow-commit](../workflow-commit/SKILL.md)；既有本機 commits 也要檢查，不能只看工作樹差異。
3. 相依 PR 使用 gh-stack 管理並核對真正增量；確認每層 base 與最後整體行為。一般 PR 沿用 repo 的分支方式。
4. 確認相關驗證已完成。尚有未完成事項時明確標示，依使用者要求及 readiness 選擇 draft 狀態。只要求草擬 PR 文案時停留在草稿。

## 建立或更新

5. 使用者要求實際建立 PR 時，將本次 branch push 到已確認的 remote；這是交付 PR 所需步驟。遇到 remote 前進先檢查差異，不能用無條件 force push 覆蓋。
6. 檢查此 repo／head 是否已有 open PR。有則更新既有 PR；無則建立，明確指定 base 與 head，避免重複或改到其他人的 PR。
7. PR 標題與描述以最終變更為準，採下方 ELI20 寫法。優先採用使用者針對本次 PR 指定的格式，其次是 repo 規範與 PR template；未指定時使用預設模板。既有 template 的欄位保留，欄位內容仍以 ELI20 說明。
8. 優先用結構化 API 傳送內容；使用 gh CLI 時，將完整 Markdown 寫到暫存檔，透過 `gh pr create --body-file` 或 `gh pr edit --body-file` 傳入。保留真正換行與程式字面值，避免把 PR body 插入 shell 命令。

## 交付確認

9. 讀回 PR URL、base、head、head SHA、draft 與狀態，核對本次內容確實存在遠端。對 stack 同時確認依賴關係。
10. 等待該 head SHA 的 CI 到終態；可用 `gh pr checks --watch`，並核對回報對應目前 head。失敗時修正授權範圍內的問題並重新確認；取消、沒有 checks、需外部核准或服務故障要如實標示。等待期間持續提供簡短進度。
11. 回報 PR 連結、SHA、驗證與 CI 結果。CI、review approval、merge、部署與使用者驗收是不同狀態；merge 及額外對外留言需有相應授權。

## ELI20 寫法

對象是有基本軟體常識、但沒參與這次開發的工程師。讓他讀完就知道為什麼改、改完會怎樣，以及憑什麼相信它有效。

- 先寫具體情境與影響，再說改動。例如「雙擊 Markdown 會因腳本沒有執行權限而失敗；安裝時補上權限，讓文件能正常開啟」。
- 用白話交代因果，第一次出現必要術語時補一句解釋。精確保留 API、欄位、命令及錯誤文字；不使用幼兒化比喻，也不只羅列檔名與實作名詞。
- 技術細節只保留 reviewer 判斷正確性與風險所需的部分。重要取捨說明原因，篇幅隨改動大小調整。
- 分清本機驗證、CI 與未驗證項目；範例、預期結果及計畫中的測試不寫成已完成。
- 描述目前交付的結果，不寫對話過程、開發流水帳或已放棄方案。

## 未指定格式時的預設

使用 [default-pr.md](templates/default-pr.md)。標題預設 `type(scope): 一句話說明具體改善`，scope 可省略；說明使用繁體中文，技術名稱保留原文。

模板的占位文字必須換成真實內容。小改動可縮成短段落，但仍交代問題、修改後行為與驗證。影響、部署步驟及關聯項目有需要才保留，不能為填滿模板捏造內容。
