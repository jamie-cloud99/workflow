# 驗證紀錄

2026-09-16，Intel macOS，本機 Python 3.11。

- 28 項測試通過：conflict 零覆寫、重複套用、原檔與 mode 還原、後續修改保留、備份歷程、併行鎖、寫入失敗復原、symlink 路徑保護、Markdown 預覽及 CLI 操作。
- latest 更新測試使用真正的本機 Git repo：先同步第一個 commit，上游新增第二個 commit 後再次同步，確認切換版本且 manifest 不需改動。
- 模擬網路失敗，確認上一份完整 resolved 清單保留；本機 source cache 被修改時不會默默覆寫或採用。
- 獨立 review 發現的同一 HEAD 新增 skill 選項問題已重現並修正；不同選用路徑使用獨立 checkout，不破壞上一份可用內容。
- 實際連線核對 6 個 GitHub 來源的最新 HEAD，下載並檢查 15 個第三方 skills。
- 7 個自有 skills 經 skill-creator 的格式驗證器檢查。
- 含中文、空白的新 home 隔離路徑：54 個設定／連結套用、再次套用、doctor、Git include 實際解析、restore 全部完成。
- 真實 home 只執行唯讀 plan，列出既有設定衝突，沒有整批替換。
- Bash/Zsh 語法及 repo 的 JSON/TOML、Python、skill metadata、文件連結納入檢查。

界線：沒有在全新實體電腦完整執行 Homebrew／Volta 安裝，沒有搬移帳號登入、測 MCP OAuth 或驗證每個第三方 skill 的實際模型行為。CI 在 Linux/macOS 測試檔案與 CLI 邏輯，不代表這些外部系統已驗收。

Markdown 預覽的本機 GUI 開檔與檔案關聯已於 2026-09-14 驗證，這次保留既有功能。
