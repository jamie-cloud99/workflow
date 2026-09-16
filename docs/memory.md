# 選用的本機記憶工具

Basic Memory 以 Markdown 保存知識、SQLite 建立索引，透過 MCP 提供讀寫與檢索。此 repo 提供選用範本；`./workflow apply` 不會自動安裝、註冊或搬移記憶。

## 安裝與資料位置

使用 Python 3.12 以上。Basic Memory 的相依條件獨立於 workflow CLI 的 Python 3.11 最低需求。

```sh
uv tool install --python 3.13 "basic-memory==0.23.2" --prerelease=allow --only-binary cryptography
basic-memory --version
```

此範本使用 Basic Memory 0.23.2。Intel macOS 的 ONNX 相依套件缺少 Python 3.14 wheel，因此此工具使用獨立 Python 3.13；不改變系統預設 Python。`--only-binary cryptography` 避免該相依套件從原始碼編譯。上游相依套件需允許預發布版本，更新前應重新驗證相容性。檢索先使用全文搜尋，不下載語意搜尋模型，也不設定雲端 provider。

```sh
export BASIC_MEMORY_FORCE_LOCAL=true
export BASIC_MEMORY_SEMANTIC_SEARCH_ENABLED=false
export BASIC_MEMORY_AUTO_UPDATE=false
export BASIC_MEMORY_NO_PROMOS=1
basic-memory project add private-memory "$HOME/basic-memory"
basic-memory project default private-memory
```

若 `private-memory` 已存在，先用 `basic-memory project list` 核對路徑，沿用或選擇其他專案名稱；不要覆蓋既有知識庫。專案改名時也需更新下方 MCP 的 `--project`。

`~/basic-memory` 是私人筆記目錄，`~/.basic-memory` 保存設定及索引。兩者都不放入公開 workflow repo。正式專案規範留在各專案 repo，記憶只保存必要摘要與來源。

## 接上 agent

- Codex：合併 [codex.example.toml](../config/basic-memory/codex.example.toml) 到使用者設定。
- Claude／支援 JSON 的 MCP client：合併 [mcp.example.json](../config/basic-memory/mcp.example.json) 的 server 定義，使用該 client 支援的註冊方式。

範本只連到 `private-memory`，明確使用本機模式、停用自動更新與語意搜尋。若 client 找不到 `basic-memory`，先執行 `command -v basic-memory`，將實際路徑填入 `command`。不要照抄另一台電腦的路徑。

不安裝自動捕捉對話的 hooks。這些是獨立選用範本，尚未納入核心 installer 的還原管理；日後以完整模板覆蓋 agent 設定時需保留這個 server 定義。

## 使用界線

需要時檢索；明確要求才新增或修改記憶。適合保存已確認決策、專案詞彙、操作經驗與交接摘要，附上來源、日期、專案及尚未確認之處。舊記憶不能凌駕目前程式碼或正式規範。

不要自動匯入完整對話、credentials 或客戶資料。接上 MCP 只提供能力，是否正確檢索與遵守寫入界線仍需在實際 client 驗證。

## 換機與還原

備份 Markdown 知識目錄，並保留專案名稱與路徑清單。可使用私人備份或私人 Git repo；多人或多機同步要先處理檔案衝突，不直接共用正在寫入的 SQLite 檔案。

新機安裝工具、還原筆記後，重新登錄專案路徑並建立索引。可用 `basic-memory project index --help` 確認該版本的索引命令，再用一筆已知筆記測試讀取與搜尋。核心 `workflow restore` 不刪除或還原這些私人資料。

## 驗證範圍與限制

隔離環境已驗證 0.23.2 的筆記新增、全文搜尋與讀回，以及 stdio MCP 初始化與工具列舉。MCP 關閉時出現 SQLite 連線清理的 `CancelledError` 訊息；本次程序結束碼為 0，但尚未驗證長期使用、多 client 並行或真實 agent 的讀寫行為。此方案保留為選用範本。

## 上游文件

[Basic Memory](https://github.com/basicmachines-co/basic-memory) 提供安裝、MCP 與本機資料管理說明。更新工具是獨立操作，不隨 `sync-skills` 更新。
