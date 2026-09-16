# 換機操作

## 1. macOS、Git 與 SSH

安裝 Xcode Command Line Tools（`xcode-select --install`）與 [Homebrew](https://brew.sh/)，再準備 Python 與 GitHub CLI：

```sh
brew install python git gh
```

新機建立自己的 SSH key，將公鑰加入 GitHub。依 [SSH 範例](../config/git/ssh.example)設定 `github-jamiecloud`，確認身分後 clone：

```sh
ssh -T git@github-jamiecloud
git clone git@github-jamiecloud:jamie-cloud99/workflow.git
cd workflow
gh auth login
gh auth status
```

GitHub 的 `ssh -T` 成功也可能 exit 1，應看回應中的帳號。若 `github.com` 已使用正確金鑰，可用 `git@github.com:jamie-cloud99/workflow.git`，不需要 alias。SSH 管理 Git 連線，gh 的 API 登入另外設定；私鑰、Git 姓名與 email 不從本 repo 自動匯入。

`brew install python` 跟隨 [Homebrew 目前穩定版](https://formulae.brew.sh/formula/python@3.14)，不鎖小版本。`./workflow` 先檢查 PATH 的 python3，再尋找版本化 Python 與 Homebrew 路徑，只要求至少 3.11。若要明確指定 interpreter，可設定 `WORKFLOW_PYTHON=/path/to/python3`。

## 2. 安裝工具

```sh
./workflow install-tools
./workflow install-tools --execute
```

第一個命令只預覽；第二個依序執行 Brewfile、Volta 管理的 Node／pnpm／CLI 與 gh-stack 安裝。任何一步失敗即停止，先前已完成的套件保留。修正後可重跑；已有 gh-stack 版本不同時，先檢查再決定是否升級。

CLI 版本仍由 `config/tools.json` 管理，專案 Node/pnpm 版本以各 repo 為準；Homebrew formula/cask 使用當時可取得版本。**第三方 skills 使用最新上游**，與 CLI 的版本策略分開。

Herdr、Docker、Playwriter Chrome extension 及 plugins 為選用，來源與理由見 `config/tools.json`。帳號／瀏覽器授權仍需新機操作。Warp 不安裝。

## 3. 取得最新 skills 並套用

```sh
./workflow sync-skills
./workflow plan
./workflow apply
```

sync-skills 每次向各 repo 查詢預設分支最新 HEAD，再下載選定 skill 目錄。全部來源成功後才更新本機使用清單；網路失敗或上游路徑移除會報錯，保留上一份完整清單。已套用的連結直到下一次 apply 才切換新版本。

repo 的 `skills/sources.json` 只記來源、路徑與分類，不固定 commit 或 checksum。本機 `~/.local/state/workflow/skills/resolved.json` 記錄實際取得的 commit 與內容摘要，供診斷及檢查 cache 是否被修改，不阻止取得更新版本。

plan 不下載、不寫設定、不建立目標目錄；顯示 create、update、unchanged、conflict。缺 skills 或衝突時 exit 2。apply 先檢查全部目的地，遇到衝突不開始改寫設定。

要採用模板取代既有設定，先讀衝突檔案與 `config/`，再執行：

```sh
./workflow apply --replace
```

會備份原檔案／leaf symlink，**不取代既有實體 skill 目錄**；需要時自行移走或合併。`.zshrc`、`.gitconfig` 保留原文，加入一個引用區塊；其他完整設定檔採模板替換，不進行任意深度 merge。

共通規則安裝到 Codex 與 Claude 的全域規則檔，skills 逐一連結到 `~/.agents/skills`、`~/.claude/skills`。舊目錄不自動清除；遷移時自行檢查同名重複項。套用後開新終端，或 `source ~/.config/workflow/env.zsh`。不搬移 Oh My Zsh cache 或既有 shell plugin。

## 4. 登入與 MCP

Codex 設定包含共用 MCP；預設模型沿用目前個人偏好，若新帳號沒有該模型，修改 `config/codex/config.toml` 再套用。沒有匯出本機 proxy、信任清單或 hook hash。

Claude MCP 使用官方 CLI 註冊，避免覆寫含登入狀態的 `.claude.json`：

```sh
codex login
claude auth login
./workflow configure-mcp
./workflow configure-mcp --execute
```

同名 MCP 但設定不同時停止，先用 `claude mcp get <name>` 檢查。新註冊 MCP 不屬於檔案 journal；移除使用 `claude mcp remove --scope user <name>`。Notion 等服務在各 client 重新 OAuth；瀏覽器及擴充套件也要在新機確認。

## 5. 檢查與預覽

```sh
./workflow doctor
./workflow doctor --online
python3 scripts/macos/install-markdown-preview.py --set-default
```

doctor 檢查設定內容與語法、skill 連結與 cache 摘要、CLI 是否存在及指定版本。`--online` 另外查 GitHub／Codex／Claude 登入；不測 MCP 連通、不發出模型請求。`--config-only` 只檢查設定。缺少或不符項目 exit 2，執行錯誤 exit 1。

[Markdown 預覽](markdown-preview.md)使用獨立的關聯備份；不依賴 Warp。

## 6. 前後端專案規則

`agents/frontend.md`、`agents/backend.md` 是專案模板，不由全域 apply 寫進專案。新 repo 可加入對應的 `AGENTS.md`，並讓 `CLAUDE.md` 指向它；既有 repo 逐段合併，保留業務與團隊政策。

## 7. 還原與演練

```sh
./workflow restore
```

restore 只回復本工具改寫的檔案、mode 與連結，或移除原本不存在的項目。後來被手動修改的內容會造成 conflict，整批還原先停止。新建空目錄、套件、skills cache、登入與 CLI 註冊的 MCP 保留。

原始內容與歷次被替換版本留在 `~/.local/state/workflow/`；還原前的 journal 另存 `restored-*.json`。這些可能含原本本機設定，不加入 Git。每份 state 只對應一個 target。

隔離演練：

```sh
./workflow plan --target '/tmp/workflow demo' --local-only
./workflow apply --target '/tmp/workflow demo' --local-only
./workflow doctor --target '/tmp/workflow demo' --local-only --config-only
./workflow restore --target '/tmp/workflow demo'
```

`--local-only` 跳過第三方 skills，供離線演練；正式換機使用完整 sync。`--state-dir` 可指定 journal/cache。工具安裝與 Claude MCP 寫入拒絕搭配非真實 home 的 target，避免演練誤動本機。
