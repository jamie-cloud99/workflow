# Workflow

我的 macOS 開發工作環境：工作規則、前後端 skills、工具設定及換機操作。

| 要找什麼 | 放哪裡 |
| --- | --- |
| AI 要遵守的規則 | [agents/](agents/) |
| 共用、前端、後端技能 | [skills/](skills/) |
| 工具設定與安裝清單 | [config/](config/) |
| 預覽、套用、檢查、還原 | [workflow](workflow) |
| 日常工作與換機說明 | [docs/](docs/) |

## 換電腦

先依[換機步驟](docs/setup.md)準備 Homebrew、Python、SSH 與登入，再執行：

```sh
git clone git@github-jamiecloud:jamie-cloud99/workflow.git
cd workflow
./workflow install-tools
./workflow install-tools --execute
./workflow sync-skills
./workflow plan
./workflow apply
./workflow doctor
```

`github-jamiecloud` 是選擇個人 GitHub 金鑰的 SSH alias，範例見 [config/git/ssh.example](config/git/ssh.example)。

第三方 skills **每次 sync 都取得上游最新版本**，不在 repo 鎖版。後續更新執行 `sync-skills`、`plan`、`apply` 即可。已有不同設定會顯示 conflict，確認後才用 `apply --replace` 備份並替換。

入口會自動找到 Python 3.11 以上版本；新機用 `brew install python` 安裝目前穩定版即可，不需要指定小版本。

## 工作方式

- [日常工作流](docs/workflow.md)：需求、除錯、review、交付。
- [Skills 清單](skills/README.md)：14 個自有 skills、26 個跟隨上游的第三方 skills。
- [Markdown 預覽](docs/markdown-preview.md)：Ghostty + Glow。
- [設計與邊界](docs/design.md)、[驗證方式](docs/verification.md)。

設定、CLI 版本、登入與 MCP 連通分別檢查；操作與驗證範圍見文件。

## 維護

```sh
python3 -m unittest discover -s tests -v
bash -n scripts/macos/preview-markdown.sh
zsh -n config/shell/env.zsh
```

本 repo 不含私鑰、token、OAuth、歷史對話或專案資料。skills 連結依賴此 repo 與下載 cache 的位置；搬動 repo 前先 restore，再從新位置 apply。
