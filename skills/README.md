# Skills

`common/`、`frontend/`、`backend/` 存放 7 個自有流程 skills；不包含 finance 專案業務資料。

`sources.json` 管理 15 個第三方 skills：gh-stack、impeccable、shadcn、playwriter、herdr、ito-explain、ito-search、ito-prd、ito-grill、ito-tdd、ito-skill，以及 React、Zod、NestJS、Supertest best practices。

## 更新方式

```sh
./workflow sync-skills
./workflow plan
./workflow apply
```

每次 sync 都向上游查詢最新 HEAD；manifest 不鎖 commit 或 checksum，也不在每次開啟 agent 時下載。下載成功後的 commit 與摘要只記在本機，方便知道用了哪一版及偵測本機 cache 修改。

若某個來源失敗或路徑被移除，上一份完整清單仍有效；不會靜默選錯其他 skill。舊 checkout 保留，apply 才切換連結。cache 有本機修改會停止，避免默默覆寫或把修改當作上游版本。

新增來源時填 repository、skill 路徑、名稱與分類，再 sync 驗證；同一階段避免多個 skill 重複接管流程。

## 舊機遷移

- 最新 impeccable 已沒有獨立的 frontend-design 目錄，使用 impeccable 入口。
- 舊 ito-issues／失效的 ito-hunt 不自行改名；需要時再選目前上游對應功能。
- Superpowers 等完整主流程未預設搬入，避免重複；保留既有安裝時，同階段仍選一個主流程。
- GitNexus CLI／MCP 已配置。舊全域 skills、codex-insights、playwright-interactive 與專案 skills 不盲目搬移，依實際需求和來源再納入。
- 第三方原始碼從作者 repo 下載，不複製提交到此 repo。授權文件與 Git 記錄隨本機 checkout 保留。
