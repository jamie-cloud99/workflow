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
7. PR 標題與描述以最終變更為準：先寫觸發問題與修改後行為，再列範圍、必要設計決策、驗證及仍存在的限制。依 repo template 填寫，不把對話過程或放棄的方案當成主要內容。
8. 優先用結構化 API 傳送內容；使用 gh CLI 時，將完整 Markdown 寫到暫存檔，透過 `gh pr create --body-file` 或 `gh pr edit --body-file` 傳入。保留真正換行與程式字面值，避免把 PR body 插入 shell 命令。

## 交付確認

9. 讀回 PR URL、base、head、head SHA、draft 與狀態，核對本次內容確實存在遠端。對 stack 同時確認依賴關係。
10. 等待該 head SHA 的 CI 到終態；可用 `gh pr checks --watch`，並核對回報對應目前 head。失敗時修正授權範圍內的問題並重新確認；取消、沒有 checks、需外部核准或服務故障要如實標示。等待期間持續提供簡短進度。
11. 回報 PR 連結、SHA、驗證與 CI 結果。CI、review approval、merge、部署與使用者驗收是不同狀態；merge 及額外對外留言需有相應授權。
