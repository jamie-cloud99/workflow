---
name: workflow-backend-contracts
description: 修改 API、授權、狀態轉換或交易寫入時使用。
---

# workflow-backend-contracts

1. 先讀入口、授權、服務與 consumer，列出成功與拒絕合約。
2. 驗證授權與可見性不是同一件事；不能以顯示用狀態決定寫入權限。
3. 明確定義重試、重複提交及並行更新的結果；以資料庫保證需要原子性的關係。
4. 更新 OpenAPI/schema 與 consumer 驗證；真實資料庫整合要確認執行而非跳過。
