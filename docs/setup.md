# 換機操作

## 1. macOS、Git 與 SSH

1. 安裝 Xcode Command Line Tools（`xcode-select --install`）與 [Homebrew](https://brew.sh/)。
2. `brew install python git gh`
3. 建立 SSH key、公鑰加入 GitHub，依 [SSH 範例](../config/git/ssh.example)設定 `github-jamiecloud`。
4. clone 並登入 gh：

   ```sh
   ssh -T git@github-jamiecloud
   git clone git@github-jamiecloud:jamie-cloud99/workflow.git
   cd workflow
   gh auth login
   ```

- `ssh -T` 成功也可能 exit 1，看回應中的帳號。
- `github.com` 已用正確金鑰時，可省略 alias。
- 私鑰、Git 姓名與 email 不由本 repo 匯入。
- Python 至少 3.11，不鎖小版本；指定 interpreter 用 `WORKFLOW_PYTHON=/path/to/python3`。

## 2. 安裝工具

```sh
./workflow install-tools            # 預覽
./workflow install-tools --execute  # 執行
```

- 順序：`brew update` → Brewfile → Volta（Node／pnpm／CLI）→ gh-stack。失敗即停，已完成的保留，修正後可重跑。
- Homebrew 套件在 `config/Brewfile`，CLI 版本在 `config/tools.json`，專案的 Node／pnpm 以各 repo 為準。
- **第三方 skills 一律用最新上游**，與 CLI 版本策略分開。
- 選用：Herdr、Docker、Playwriter extension、plugins（見 `config/tools.json`）。帳號與瀏覽器授權需在新機操作。Warp 不安裝。

### 新專案的驗證工具

launch／drive／observe（啟動、操作、讀回結果）的工具因專案而異，放在各專案 repo，不放在本 repo。需要用真實操作證明 UI、CLI 或服務行為時，先用專案已有的 verification／run skill；沒有就在新專案執行一次 pstack 的 `create-verification-skill`（plugin：`/plugin marketplace add michael-denyer/pstack-claude`，再 `/plugin install pstack@pstack-claude`），並把產生的 skill 提交到該專案。

## 3. 取得 skills 並套用

```sh
./workflow sync-skills
./workflow plan
./workflow apply
```

**sync-skills**
- 取各 repo 預設分支最新 HEAD，全部成功才更新本機清單；失敗則保留上一份。
- 連結要等下次 apply 才切到新版。
- `skills/sources.json` 只記來源，不鎖 commit；實際 commit 與摘要記在 `~/.local/state/workflow/skills/resolved.json`，僅供診斷。

**plan**：不寫入任何東西，列出 create／update／remove／unchanged／conflict；缺 skills 或衝突時 exit 2。

**apply**
- 先檢查全部目的地，有衝突就不改寫。
- 規則裝到 Codex 與 Claude 全域規則檔；skills 連結到 `~/.agents/skills`、`~/.claude/skills`。
- 退役的 skill 只移除本工具管理的連結；手動安裝的與被改動的連結保留或回報 conflict。
- 套用後開新終端。

| 選項 | 作用 |
| --- | --- |
| `--skills-only` | 只處理 skills 連結，不碰設定、shell、git 檔案，其他檔案衝突不擋 |
| `--local-only` | 跳過第三方 skills |
| `--replace` | 用模板取代既有設定（先讀衝突檔與 `config/`） |

`--replace` 會備份原檔，**不取代既有實體 skill 目錄**；`.zshrc`、`.gitconfig` 只加一個引用區塊，其他設定檔整份替換。

### zsh 與 Herdr

`.zshrc` 的 `# workflow:start`／`# workflow:end` 區塊載入 `~/.config/workflow/` 下的設定，區塊外內容保留。

| 維護位置 | 套用位置 | 用途 |
| --- | --- | --- |
| `config/shell/env.zsh` | `~/.config/workflow/env.zsh` | PATH、Volta |
| `config/shell/interactive.zsh` | `~/.config/workflow/interactive.zsh` | 補完、歷史、prompt、fzf、zoxide、autosuggestions |
| `config/shell/p10k.zsh` | `~/.config/workflow/p10k.zsh` | 配色、分隔符號、中文 Git 狀態 |
| `config/herdr/config.toml` | `~/.config/herdr/config.toml` | Catppuccin、通知、關閉音效 |

- Brewfile 安裝 fzf、zoxide、zsh-autosuggestions、[Powerlevel10k](https://formulae.brew.sh/formula/powerlevel10k)；未安裝的工具會跳過。新機不需 Oh My Zsh，已有的沿用。
- 受管理區塊要放在既有 shell／plugin 初始化之後。
- 新終端確認正常後，可刪掉舊的 fzf／zoxide／autosuggestions 載入段落。
- `~/.p10k.zsh` 不改寫；改 `config/shell/p10k.zsh` 後重新 apply。
- Herdr 為選用，apply 只寫設定。已執行的 session 在 pane 內執行 `herdr server reload-config`。
- 選用的 [Auto Title](https://github.com/kryptamine/herdr-auto-title)：裝 Go 後在 pane 內執行 `herdr plugin install kryptamine/herdr-auto-title`（裝的是當時上游版本）。plugin 需待 server 下次啟動才載入，首次啟動可能覆寫既有名稱。
- Matt Pocock 的 skills：每個專案第一次使用前執行 `setup-matt-pocock-skills`。

## 4. 登入與 MCP

```sh
codex login
claude auth login
./workflow configure-mcp            # 預覽
./workflow configure-mcp --execute
```

- Codex 預設模型沿用個人偏好，新帳號沒有就改 `config/codex/config.toml`。
- Claude MCP 用官方 CLI 註冊；同名但設定不同時會停止，先 `claude mcp get <name>`。
- 移除：`claude mcp remove --scope user <name>`。
- Notion 等服務需在各 client 重新 OAuth。

## 5. 檢查與預覽

```sh
./workflow doctor            # 設定、skill 連結、CLI 版本
./workflow doctor --online   # 另查 GitHub／Codex／Claude 登入
python3 scripts/macos/install-markdown-preview.py --set-default
```

- `--config-only` 只檢查設定。缺少或不符 exit 2，執行錯誤 exit 1。
- 不測 MCP 連通、不發模型請求。
- [Markdown 預覽](markdown-preview.md)不依賴 Warp。

## 6. 前後端專案規則

`agents/frontend.md`、`agents/backend.md` 是模板，不由 apply 寫進專案。新 repo 加入 `AGENTS.md` 並讓 `CLAUDE.md` 指向它；既有 repo 逐段合併。

## 7. 還原與演練

```sh
./workflow restore
```

- 只回復本工具改寫的檔案、mode、連結。之後被手動修改的內容會 conflict，整批停止。
- 不動：空目錄、套件、skills cache、登入、已註冊的 MCP。
- 備份與 journal 在 `~/.local/state/workflow/`，可能含本機設定，不要加入 Git。

隔離演練（工具安裝與 MCP 寫入拒絕非真實 home 的 target）：

```sh
./workflow plan --target '/tmp/workflow demo' --local-only
./workflow apply --target '/tmp/workflow demo' --local-only
./workflow doctor --target '/tmp/workflow demo' --local-only --config-only
./workflow restore --target '/tmp/workflow demo'
```
