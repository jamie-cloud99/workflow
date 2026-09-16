---
name: workflow-commit
description: 使用者要求 commit、提交變更、整理提交，或已授權 ship 流程需要建立 commit 時使用；只詢問建議訊息時提供文案。
---

# workflow-commit

建立範圍清楚、已驗證、可獨立理解的提交，保留工作樹中其他人的工作。

## 提交流程

1. 讀取 repo 的提交規範與最近 commit 風格。確認目前分支、`git status --short`、staged diff、unstaged diff 及本次新增檔案，辨識哪些屬於任務。
2. 依用途拆分提交。每個 commit 應是一個可理解的變更；使用明確檔案或選定 hunks staging。同一檔案若混有無關修改，只提交可明確分離的部分。
3. 既有 staged 內容若不屬於本任務，保留其內容與 staging 狀態；必要時使用隔離工作樹。無法辨識提交範圍時，指出具體檔案與差異再詢問，不能自行清空 index、stash 或丟棄修改。
4. 執行 repo 規定及與變更相符的驗證，再檢查 `git diff --cached --check` 與完整 staged diff。確認提交不含 credentials、暫存產物或無關檔案。lint-staged 需要先 stage 才有檢查效果。
5. commit message 優先採用使用者本次指定格式，其次是 repo 提交規範；未指定時使用下方預設模板。主旨說明具體改變，需要時在 body 說明原因、行為與限制。變更歷史寫在 commit；README 只描述現況。
6. 使用者已要求提交時，直接建立 commit，不再要求批准訊息。保留正常 hooks；失敗時找出原因、修正並重跑相關驗證。amend、rebase 等改寫既有提交的操作須符合既有授權與分支狀況。
7. 讀回 commit SHA、內容與檔案範圍，重新查看工作樹及 index，確認其他工作仍在。回報 SHA、驗證結果與未包含的任務修改。

## 與交付流程銜接

單純 commit 完成於本機提交。使用者另有 push／PR／ship 授權時繼續該流程；建立或更新 PR 使用 [workflow-create-pr](../workflow-create-pr/SKILL.md)。沒有任務差異時回報現況，不建立空 commit。

## 未指定格式時的預設

使用 [default-commit.txt](templates/default-commit.txt)。採 Conventional Commits 外形，說明文字預設繁體中文，技術名稱保留原文：

- 主旨為 `type(scope): 具體改變`；scope 可省略。
- type 依主要改動選 feat、fix、refactor、docs、test 或 chore，不混用來誇大影響。
- 小改動只需主旨。body 的原因、變更、驗證及關聯依需要保留，不留下空欄位或未替換的占位文字。
- 只填實際執行的驗證；有關聯 issue 才填，不能推測編號或連結。
