# Markdown 預覽

雙擊 `.md` 或 `.markdown`，會在 Ghostty 開啟排版預覽。標題、清單、表格與程式碼會套用終端機樣式；用方向鍵、Page Up/Down 捲動，按 `q` 關閉。

這是文字終端機預覽，圖片不會顯示，Mermaid 不會轉成圖形；它也不編輯原文件。來源檔更新後需重新開啟。

### 換機安裝

需要 macOS、Homebrew、Python 3 與 AppleScript 編譯工具。請在一般 Terminal/Ghostty 執行，不在限制 AppleScript/LaunchServices 的 agent sandbox 內執行。

目前使用 `github-jamiecloud` SSH alias，確保選到 `jamie-cloud99` 的金鑰。新機先在 GitHub 帳號加入自己的公鑰，再於 `~/.ssh/config` 設定（`IdentityFile` 改成新機實際金鑰路徑）：

```sshconfig
Host github-jamiecloud
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_jamiecloud
  IdentitiesOnly yes
```

如果新機的 `github.com` 本來就使用正確帳號，也可以直接用 `git@github.com:jamie-cloud99/workflow.git`，不需要 alias。SSH 私鑰不收進 repo。

```sh
git clone git@github-jamiecloud:jamie-cloud99/workflow.git
cd workflow
brew install --cask ghostty
brew install glow duti python
python3 scripts/macos/install-markdown-preview.py --set-default
open docs/design.md
```

若 Ghostty 已安裝可跳過 cask 安裝。腳本支援 Homebrew 的 Intel 與 Apple Silicon 路徑。Homebrew 指令安裝當時可取得的版本。

預覽 app 安裝至 `~/Applications/Markdown Preview.app`，包含閱讀腳本；安裝後可移動 repo，不影響預覽器。

省略 `--set-default` 只安裝 app，不主動設定預設程式：

```sh
python3 scripts/macos/install-markdown-preview.py
open -a 'Markdown Preview' README.md
```

若原本沒有可查詢的 Markdown 預設程式，`--set-default` 會在更動關聯前停止。可先用 Finder 的「取得資訊 → 打開檔案的應用程式 → TextEdit → 全部更改」建立基準，再執行安裝。

### 確認設定

```sh
duti -x md
duti -x markdown
```

兩者都應顯示 `Markdown Preview`，bundle ID 為 `com.jamiecloud99.workflow.markdown-preview`。

### 還原或改用 TextEdit

原本的有效預設應用程式記錄在：

```text
~/Library/Application Support/dev-workflow/markdown-preview/defaults-before.json
```

重裝不覆寫這份記錄，既有 app 另存成 ZIP 備份。若原應用程式仍在，可執行：

```sh
python3 scripts/macos/install-markdown-preview.py --restore-defaults
```

還原的是副檔名的有效預設 app，不是完整的 macOS LaunchServices 狀態或分角色偏好。如果你已手動改成其他 app，還原器會保留現況並回報衝突。

要將預設開啟程式設為 TextEdit：

```sh
duti -s com.apple.TextEdit .md all
duti -s com.apple.TextEdit .markdown all
```

預覽 app 與工具不會因還原關聯而被卸載。備份及帳號狀態不進 Git。

## 開發驗證

```sh
python3 -m unittest discover -s tests -v
bash -n scripts/macos/preview-markdown.sh
```

可在暫存目錄驗證編譯，不變更預設關聯：

```sh
python3 scripts/macos/install-markdown-preview.py \
  --app-dir /tmp/workflow-preview-check/Applications \
  --state-dir /tmp/workflow-preview-check/state
```

macOS 會註冊 app；完成後先用系統 `lsregister -u` 取消該測試 app 的註冊，再刪除自己建立的暫存目錄，避免留下同 bundle ID 的測試副本。

## 來源

- [Glow](https://github.com/charmbracelet/glow)：終端機 Markdown 排版與分頁閱讀。
- [Ghostty configuration](https://ghostty.org/docs/config/reference#initial-command)：透過 `-e` 啟動閱讀器。
- duti 的使用方法以安裝版本的 `man duti` 為準。
