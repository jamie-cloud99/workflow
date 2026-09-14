# 可攜式開發工作環境

狀態：整體設計草案；Markdown 預覽子項目已進入實作，其餘完整環境安裝器尚未實作。

## 目標與已確認範圍

以 `jamie-cloud99/workflow` repo 管理 macOS 開發環境，包含 Codex、Claude Code、共用 agent 規則、前後端 skills、MCP、Git、終端機及工具安裝。換機後能從 repo 重建工作方式，並清楚知道哪些項目還需登入或手動完成。

使用者已確認涵蓋完整開發環境，以 macOS 為第一版。以下為建議設計，尚未代表使用者逐項同意。

## 方案比較

| 方案 | 優點 | 代價 |
| --- | --- | --- |
| 分層設定 repo + 小型安裝器（建議） | 工作流程、skills、工具來源與換機步驟集中管理；容易閱讀與逐項驗證 | 需要維護設定轉換與衝突處理 |
| 純設定備份 + 手動安裝文件 | 建立成本低 | 換機要手動修路徑、重建連結，難確認是否恢復完整 |
| 完整 dotfiles 管理框架 | 適合大量系統設定與跨機器差異 | 多一套工具與模板規則；本次先不增加這個依賴 |

## 本機盤點結果

盤點日期：2026-09-14。以下來自檔案結構、設定鍵名、symlink 狀態及命令路徑；命令存在不代表功能已驗證。

- 使用者 skills 分散於 `~/.agents/skills`、`~/.codex/skills`、`~/.claude/skills`。
- `~/.agents/.skill-lock.json` 有部分 skills 的來源及內容 hash；內容 hash 不可直接當成來源 repo 的 commit。
- `find-skills` 在 Codex 與 Claude 的連結皆失效，Claude 的 `ito-hunt` 連結亦失效。
- `superpowers` 連結指向本機 Codex 目錄中的絕對路徑。
- Codex 設定包含 MCP、plugins、專案信任路徑及 hook 信任狀態；全域 `AGENTS.md` 是空檔。
- Claude 全域規則包含 GitNexus 的本機絕對路徑；Codex 與 Claude hooks 也有絕對路徑。
- Codex 的 MCP 名稱包含 notion、playwright、chrome-devtools、gitnexus；Claude 全域 MCP 名稱包含 deepwiki、context7、gitnexus。
- 目前 `node`、`pnpm`、`npm`、`codex`、`gitnexus`、`playwriter` 由 Volta bin 路徑提供。
- `~/.config/Brewfile` 仍列有 Node 14、nvm、MySQL 5.7、舊 OpenSSL 等項目，不能直接視為新機安裝清單。
- `finance-system/package.json` 宣告 `pnpm@10.28.0`；`finance-system-ui/package.json` 的 Volta 設定指定 Node `22.22.2`、pnpm `10.33.0`。專案版本需求不強制改成同一組全域版本。
- 後端現有 skills 包括 API、DDD、資料庫、測試、安全、PR 等；前端有元件、API 相容、Zod、單元測試、瀏覽器 QA 等 skills，並有獨立 governance 文件。

## 建議目錄與責任

以下是預定結構，並非已實作檔案。

```text
workflow/
  README.md
  agents/                 # 共通規則、角色指引、skill routing
  workflows/              # feature、bugfix、review、ship、handoff
  skills/local/           # 自有或已確認可維護的客製 skills
  manifests/              # 第三方 skills、plugins、CLI 來源與版本
  templates/projects/     # frontend、backend 的可攜式專案起始模板
  config/codex/           # 經挑選的設定模板
  config/claude/           # 經挑選的設定模板
  config/mcp/              # 服務定義與需要的環境變數名稱
  config/git/
  config/shell/
  config/terminal/
  tools/                  # 核心與選用的工具清單
  scripts/                # plan、apply、doctor、restore
  docs/                   # 換機操作、來源盤點、驗收與設計
```

## Agent 與 workflow

共通規則只放跨專案成立的原則：繁體中文溝通、任務範圍、保留既有工作、驗證與交付證據。角色指引涵蓋需求、架構、工程、QA 與使用者角度；角色不等於每次任務都啟動多個 agent。

工作流程分為需求到交付、除錯、PR review、提交與 CI、工作交接。每一流程說明輸入、下一步、驗證方式及完成條件，避免多個 skills 對同一階段重複要求訪談、計畫或確認。

規則有三個維護層次：個人共通規則、前後端模板、專案規則。前後端模板不包含財務專用工具類別、表名或業務政策；這些仍留在原專案。模板只在新專案或明確指定的專案套用，不由全域安裝器改寫既有 repo。

## Skills 與第三方來源

個人共用 skills 以單一來源管理，再依執行環境建立連結。Codex 以官方文件列出的使用者 `.agents/skills` 作為主要安裝位置，避免再安裝另一份同名 skill。Claude 的安裝位置與 metadata 於實作前對照其官方文件驗證。

第三方來源清單記錄 repository、已驗證 revision、skill 子路徑、內容 checksum、適用環境及依賴。更新是明確操作，不在每次啟動時追蹤 latest。上游版本與本機修改分開記錄；找不到來源者先保留盤點狀態，不假裝已可重建。

失效連結需確認來源後才能納入安裝項目；已由 plugin 提供的 skill 不重複安裝。第三方內容若需收錄，保留來源與授權文件。

## 工具與設定

核心清單涵蓋 Git、gh、搜尋與 JSON 工具、Node 工具鏈、Codex、Claude Code。沿用 Volta 作為 Node 工具鏈管理方式，實作時驗證安裝途徑。MCP、瀏覽器工具、Docker、終端機外觀及其他工具分組選用，舊專案依賴另行記錄。

使用者已指定 Markdown 使用排版預覽；第一個工具子項目採 Ghostty + Glow。Warp 已預計移除，不列入新環境安裝依賴；其既有 plugin/hook 若出現在盤點中，列為退役候選，不能因舊設定存在就自動搬移或啟用。

Intel 與 Apple Silicon 的 Homebrew 路徑於安裝時偵測。架構不支援的套件顯示原因，不自動套用另一架構的二進位檔。各工具以明確版本或可追溯安裝來源管理；Homebrew 項目若無法保證精確版本，文件說明限制。

設定模板以允許清單挑選欄位，轉換成工具原生設定格式。不得假設 TOML 或 JSON 本身會展開所有環境變數；安裝器負責需要的路徑替換及格式檢查。

token、OAuth、SSH/GPG 私鑰、歷史 session、快取、專案信任紀錄及 hook 信任 hash 不加入 repo。MCP 僅收錄服務與憑證需求，登入或授權由新機完成。模型、provider、權限偏好保留可配置能力，不直接複製無法驗證或只適用本機的欄位。

## 換機操作草案

以下描述預期功能，目前尚不可執行。

1. Clone repo，確認 macOS、CPU 架構及必要的初始安裝條件。
2. 執行 `plan`：列出將安裝的工具、建立的連結、產生的設定、衝突檔案及需登入的服務；不改動系統。
3. 執行 `apply`：安裝選定項目，產生經驗證的設定，建立 skills 連結，逐項記錄結果。
4. 既有檔案有不同內容時，預設保留並回報衝突；明確選擇替換時先備份。備份及操作紀錄放在 repo 外的本機狀態目錄。
5. 登入 GitHub、Codex、Claude 及選用的 MCP；瀏覽器擴充等手動工作提供明確步驟。
6. 執行 `doctor`：檢查工具版本、設定解析、連結目標及選用服務狀態。區分「設定可讀」「CLI 可用」「登入完成」「服務連通」，不以其中一項代表全部完成。

再次執行 apply 不重複寫入 shell 設定或新增同名連結。網路或套件安裝失敗時保留已完成結果並回報未完成項目，不能宣告全數成功。`restore` 只還原本工具管理的檔案及連結，並在使用者後續修改時回報衝突；不卸載共用套件或刪除資料庫。

## 驗收範圍

- 可在暫存目標目錄驗證設定產生及連結建立，不需要先修改目前 home。
- 在不同使用者名稱及含空白路徑下，產生的設定不含舊機 home 路徑。
- 重複套用結果一致；遇到既有不同內容會保留並回報。
- 還原能恢復原檔案，且不覆寫安裝後的額外修改。
- 缺工具、失效連結、缺憑證、網路失敗均有可區分的診斷。
- 版本清單與實際取得的第三方內容一致；repo 不含登入資料及機器狀態。
- macOS 真機完整安裝與暫存目錄驗證分開報告；未測架構不得宣稱已驗證。

## 交付順序與界線

設計確認後，先交付 repo 基礎文件、來源清單及共通規則，再交付設定模板與 skills 整理，最後完成安裝與驗證工具。第一版不重建專案資料庫內容，也不遷移歷史對話。

使用者已指定遠端 `https://github.com/jamie-cloud99/workflow`。Markdown 預覽以 Ghostty + Glow 作為第一個可獨立交付的工具設定；repo 不改變遠端可見性。原始設定尚未批次匯出，其餘環境套用待後續實作。

## 官方依據

- [Codex Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)：使用者與專案設定層次，以及專案信任的關係。
- [Codex Build skills](https://learn.chatgpt.com/docs/build-skills)：使用者 skills 位置、symlink 支援，以及同名 skills 不自動合併。

尚待使用者確認的是上述整體設計。各工具確切版本、來源及可攜欄位由實作時逐項查證後填入 manifests；不得將未查證項目標成可安裝。
