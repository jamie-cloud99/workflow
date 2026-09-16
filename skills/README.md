# Skills

`common/`、`frontend/`、`backend/` 存放 14 個自有 skills。`sources.json` 管理 24 個第三方 skills 的來源、路徑與分類。

流程型 skills 使用 `workflow-` 前綴，例如交付、review、prototype、瀏覽器驗收與資料庫變更；架構方法及契約規範直接使用主題名稱，例如 `ddd`、`bdd`、`frontend-contracts`、`backend-contracts`。第三方 skills 沿用上游名稱。

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

| [1weiho/open-slide](https://github.com/1weiho/open-slide) | create-slide、slide-authoring、current-slide、apply-comments、create-theme |

| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | open-code-review-delegate |

## 主要入口

| 需求 | 入口 |
| --- | --- |
| 實作交付、交付前自查與交接 | [workflow-delivery](common/workflow-delivery/SKILL.md) |
| 自己的變更自查、擔任 reviewer、處理 review 回饋 | [workflow-review](common/workflow-review/SKILL.md) |
| 建立 commit、整理提交範圍 | [workflow-commit](common/workflow-commit/SKILL.md) |
| 建立／更新 GitHub PR、確認遠端 CI | [workflow-create-pr](common/workflow-create-pr/SKILL.md) |
| 調查原始碼、官方文件與 API | research |
| Prototype／POC 驗證互動或狀態模型 | [workflow-prototype](common/workflow-prototype/SKILL.md) |
| 需求訪談 | grill-me；由 grilling 執行 |
| 彙整已討論內容為 spec | to-spec |
| Test-first 開發 | tdd；codebase-design 提供介面設計語彙 |
| 撰寫 skill 與 agent 文件 | writing-for-agents |
| 專案 tracker 與文件位置設定 | setup-matt-pocock-skills |
| 製作 open-slide 簡報與主題、處理頁面註解 | create-slide、slide-authoring、current-slide、apply-comments、create-theme |
| 精簡回覆 | caveman |

Matt Pocock 的工程 skills 第一次用於某專案前，執行 `setup-matt-pocock-skills` 設定 tracker 與文件位置。對外發佈仍依使用者授權。

commit／PR 未指定格式時，分別使用 [commit 模板](common/workflow-commit/templates/default-commit.txt)與 [PR 模板](common/workflow-create-pr/templates/default-pr.md)。PR 以 ELI20 交代情境、改動後行為與驗證，已有 repo template 時沿用欄位。

`/caveman` 啟用精簡回覆，保留技術資訊、命令、錯誤與使用者指定語言；`/caveman off` 關閉。本清單使用主 skill。

open-slide skills 使用上游 `packages/core/skills/`，需在 open-slide 簡報專案內使用；同步 skills 不會安裝簡報 runtime。新簡報專案可依[上游說明](https://github.com/1weiho/open-slide)使用 `npx @open-slide/cli init my-slide` 建立，專案內 skills 已存在時沿用專案版本，避免重複維護。

open-code-review-delegate 是選用 review 輔助：由 `ocr` 提供檔案範圍與規則，目前 agent 負責審查。使用前需另行安裝 `ocr`（見 `config/tools.json` 的選用工具）；delegate 不需額外 LLM endpoint。需要覆蓋清單或按檔案匹配規則時才使用，仍由 workflow-review 決定角色與授權，且需核實 findings；檔案覆蓋率不等於缺陷召回率。

## 按需選用

下列 skills 是可選的專業指引，已安裝不代表每個任務都要使用。使用者要求、專案已採用且改動涉及其邊界，或任務有明確需求時才選用；一般 CRUD、文件與小修正不需套用整套方法。

| Skill | 適用情境 | 不預設引入 |
| --- | --- | --- |
| [ddd](backend/ddd/SKILL.md) | 領域語言、bounded context、aggregate 與不變條件 | 微服務、完整 DDD 樣板 |
| [cqrs](backend/cqrs/SKILL.md) | 讀寫模型需要分離或維護既有 CQRS | Event Sourcing、獨立資料庫、eventual consistency |
| [hexagonal-architecture](backend/hexagonal-architecture/SKILL.md) | 以 ports／adapters 隔離核心與外部依賴 | 每個類別都建立 interface、多餘分層 |
| [bdd](common/bdd/SKILL.md) | 透過具體例子釐清行為與驗收 | Cucumber、全部改寫為 E2E、重複需求訪談 |

可依情境組合，但不互相強制載入。每個 skill 只保留精簡決策指引，原始概念來源在各文件內按需參考。導入新架構仍限於任務範圍，不因選用 skill 擴大成全面重構。

## 同步與套用

```sh
./workflow sync-skills
./workflow plan
./workflow apply
```

每次 sync 都查詢上游最新 HEAD。repo 不鎖 commit 或 checksum；實際取得的版本與摘要保存在本機。來源失敗時保留上一份完整清單，apply 才切換連結；cache 有本機修改時會停止。

`retired_skills` 指定不再啟用的名稱。apply 只移除本工具管理且未被修改的連結；手動安裝的目錄及未管理連結保留，衝突需先處理。相關操作見[換機說明](../docs/setup.md)。

新增來源時填 repository、skill 路徑、名稱與分類，再 sync 驗證。第三方原始碼、授權文件與 Git 記錄保存在本機 checkout。
