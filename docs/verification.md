# 驗證方式與範圍

## 本機

使用 Python 3.11 以上執行：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check.py
bash -n workflow
bash -n scripts/macos/preview-markdown.sh
zsh -n config/shell/env.zsh
zsh -n config/shell/interactive.zsh
zsh -n config/shell/p10k.zsh
```

測試涵蓋 Python 自動選擇、檔案衝突、重複套用、備份還原、後續修改保留、寫入中斷復原、鎖定、symlink、第三方 skills 更新及退休連結清理。Git 來源測試建立真正的本機 repository，驗證上游版本變動、選用路徑變動與失敗時保留可用清單。

check.py 驗證 JSON/TOML、Python 語法、自有 skill metadata 與 Markdown 連結。

## 隔離演練

```sh
./workflow plan --target '/tmp/workflow review' --local-only
./workflow apply --target '/tmp/workflow review' --local-only
./workflow doctor --target '/tmp/workflow review' --local-only --config-only
./workflow restore --target '/tmp/workflow review'
```

要驗證第三方來源，對同一個 target 執行 sync-skills，並省略後續操作的 local-only。只在暫存 target 做套用／還原測試；確認 source cache、連結與 Git include 都使用該目標的路徑。

## CI

GitHub Actions 在 Linux/macOS 與 Python 3.11/3.14 執行測試、語法檢查及 launcher 預覽。實際結果查對應 commit 的 [Checks](https://github.com/jamie-cloud99/workflow/actions)。

CI 不執行完整 Homebrew 安裝、帳號登入、MCP OAuth 或模型請求。這些項目需依新機的實際環境另行驗證。

## Markdown 預覽

安裝器測試檢查 script 執行權限、原預設程式備份及關聯更新的確認。macOS 真機需另外開啟 Markdown 文件，確認預設 app、文件參數與畫面內容；只有 open 成功或程序存在不足以證明畫面已正確呈現。
