# Skills

`common/`、`frontend/`、`backend/` 存放 9 個自有流程 skills。`sources.json` 管理 18 個第三方 skills 的來源、路徑與分類。

## 第三方來源

| 來源 | Skills |
| --- | --- |
| [github/gh-stack](https://github.com/github/gh-stack) | gh-stack |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | impeccable |
| [shadcn/ui](https://github.com/shadcn/ui) | shadcn |
| [remorses/playwriter](https://github.com/remorses/playwriter) | playwriter |
| [herdrdev/herdr](https://github.com/herdrdev/herdr) | herdr |
| [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) | caveman |
| [mattpocock/skills](https://github.com/mattpocock/skills) | research、grill-me、grilling、to-spec、tdd、codebase-design、writing-for-agents、setup-matt-pocock-skills |
| [steveonead/agent-skills](https://github.com/steveonead/agent-skills) | react-best-practices、zod-best-practices、nestjs-best-practices、supertest-best-practices |

## 主要入口

| 需求 | 入口 |
| --- | --- |
| 建立 commit、整理提交範圍 | [workflow-commit](common/workflow-commit/SKILL.md) |
| 建立／更新 GitHub PR、確認遠端 CI | [workflow-create-pr](common/workflow-create-pr/SKILL.md) |
| 調查原始碼、官方文件與 API | research |
| 需求訪談 | grill-me；由 grilling 執行 |
| 彙整已討論內容為 spec | to-spec |
| Test-first 開發 | tdd；codebase-design 提供介面設計語彙 |
| 撰寫 skill 與 agent 文件 | writing-for-agents |
| 專案 tracker 與文件位置設定 | setup-matt-pocock-skills |
| 精簡回覆 | caveman |

Matt Pocock 的工程 skills 第一次用於某專案前，執行 `setup-matt-pocock-skills` 設定 tracker 與文件位置。對外發佈仍依使用者授權。

commit／PR 未指定格式時，分別使用 [commit 模板](common/workflow-commit/templates/default-commit.txt)與 [PR 模板](common/workflow-create-pr/templates/default-pr.md)。PR 以 ELI20 交代情境、改動後行為與驗證，已有 repo template 時沿用欄位。

`/caveman` 啟用精簡回覆，保留技術資訊、命令、錯誤與使用者指定語言；`/caveman off` 關閉。本清單使用主 skill。

## 同步與套用

```sh
./workflow sync-skills
./workflow plan
./workflow apply
```

每次 sync 都查詢上游最新 HEAD。repo 不鎖 commit 或 checksum；實際取得的版本與摘要保存在本機。來源失敗時保留上一份完整清單，apply 才切換連結；cache 有本機修改時會停止。

`retired_skills` 指定不再啟用的名稱。apply 只移除本工具管理且未被修改的連結；手動安裝的目錄及未管理連結保留，衝突需先處理。相關操作見[換機說明](../docs/setup.md)。

新增來源時填 repository、skill 路徑、名稱與分類，再 sync 驗證。第三方原始碼、授權文件與 Git 記錄保存在本機 checkout。
