# 可攜式工作環境實作

設計已於 2026-09-16 確認，沿用五目錄。以下工作在同一分支依序完成。

1. 整理 `agents/common.md`、`frontend.md`、`backend.md` 及 `docs/workflow.md`，將共通習慣與專案政策分開。新增少量自有 skills；第三方 skills 依使用者新指示每次 sync 使用上游最新版本；僅在本機記錄取得結果。
2. 在 `config/` 建立 Codex、Claude、Git、Ghostty、shell、MCP 與工具清單。只輸出明確挑選的設定，不匯出原始帳號資料或 Warp hooks。使用者已授權的路徑與帳號透過新機本機設定提供。
3. 先寫 `tests/test_managed_files.py`，涵蓋 plan 零寫入、衝突零覆寫、重複套用、備份還原、安裝後修改保留、父目錄 symlink 與併行執行。用暫存目錄做真實檔案測試。
4. 實作 `scripts/managed_files.py`：原子寫入、逐檔 journal、互斥鎖、已管理檔案更新前比對、還原只移除本工具產生且未修改的內容。
5. 實作 `scripts/workflow.py`：`plan`、`apply`、`doctor`、`restore`、`sync-skills`、`install-tools`、`configure-mcp`。`--target` 支援沙盒演練；工具安裝與 Claude MCP 設定需明確 `--execute`，不由 apply 偷跑安裝或登入。
6. 驗證 skills 可實際取得上游最新 HEAD，本機記錄實際 commit 與內容摘要；驗證 TOML/JSON、shell 語法、所有 Markdown 內部連結及本機隔離安裝還原。缺少登入／服務連通不得報成全部正常。
7. 更新 README 與 `docs/setup.md`，用一套直接操作步驟說明預覽、衝突、安裝、登入、檢查與還原。更新 CI，推送指定 SSH repo，確認 exact commit 的遠端結果。

驗收：完整換機路徑可執行、重跑不重複設定、不覆寫未知內容、來源版本可追溯、登入資料不進 Git。目前電腦只做唯讀盤點與暫存目錄演練，不整批改寫既有 home。
