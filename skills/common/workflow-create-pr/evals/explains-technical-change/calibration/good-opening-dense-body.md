# 測試 PR 交付流程

當你請 AI 幫忙提交修改並建立 PR，它可能把你留給其他工作的修改一起提交，或把舊版本通過的測試當成新版本已經通過。這次加入幾道模擬題，檢查 AI 寫出的做法是否會犯這些錯誤。

## 評測方式

with-plugin arm 以 scaffold 配置 fixture，針對 exact-head trace 執行 grader assertions；baseline arm 不載入 delivery/commit/create-pr chain，並以 per-case macro average 聚合 benchmark。publication gate 另驗 remote headRefOid 與 terminal checks，避免 stale SHA 的 rollup 被解讀為新 head 的驗證證據。

## 結果

有提供指引時通過 11 項評分條件，沒有提供時通過 9 項。差異是繁體中文與標題格式。安全條件兩組都通過，不能據此說實際交付更安全。
