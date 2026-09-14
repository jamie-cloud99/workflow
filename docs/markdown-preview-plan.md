# Markdown 預覽實作計畫

目標：雙擊 Markdown 文件時，以 Ghostty + Glow 顯示終端機排版預覽；保存可重建的設定與原預設應用程式。

架構：AppleScript app 接收 Finder 的文件開啟事件，使用安全引號將路徑傳給 Ghostty；app 內附 Bash 腳本執行 Glow。Python 安裝器編譯 app、保留既有安裝與有效預設程式，並透過 duti 設定及檢查關聯。此子項目先在本次 session 內完成。

1. 建立 `tests/test_markdown_preview.py`，驗證含空白、Unicode、shell 特殊字元的文件路徑能原樣傳遞，缺檔與目錄不會啟動閱讀器。先執行 `python3 -m unittest discover -s tests -v` 確認失敗。
2. 建立 `scripts/macos/preview-markdown.sh`，只接受一個本機可讀 Markdown 檔案，以 `glow -p` 顯示，明確使用 `less -R`。以同一測試命令驗證。
3. 建立 `config/macos/Markdown Preview.applescript` 與 `scripts/macos/install-markdown-preview.py`。以 `--app-dir` 支援暫存位置；預設不變更檔案關聯，明確傳入 `--set-default` 才套用。重裝先備份原 app；`--restore-defaults` 只回復已保存的有效預設應用程式，不移除共用套件。
4. 實際編譯 app，檢查 Info.plist 與 app 內的閱讀腳本。安裝至使用者 Applications，查證 `duti -x md` 與 `duti -x markdown`。
5. 使用 `open` 開啟規劃文件，確認 Ghostty/Glow/less 程序有正確檔案，並驗證 Glow 可排版中文文件。GUI 若無法直接目視，明確報告驗證限制。
6. 將原設計草案收進 repo，補 README、換機及還原指令、終端機不支援圖片/Mermaid 的限制。執行測試、語法檢查與 `git diff --check`，再 commit/push 至使用者指定遠端。

本子項目不代表整套 agents/skills/工具環境已整理完畢；整體設計文件仍作為後續建置依據。
