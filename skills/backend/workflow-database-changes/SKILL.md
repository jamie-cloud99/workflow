---
name: workflow-database-changes
description: 建立 migration、資料回填、批次同步或排查資料庫鎖時使用。
---

# workflow-database-changes

1. 先確認目標環境、版本、表名、資料量與可回復方式；不得把讀到的文件名稱當成已驗證 schema。
2. 使用專案 migration 產生工具，保留已共享或已套用檔案的身分。
3. 評估 metadata lock、長交易、索引與部署順序。需要終止連線或破壞性寫入時，先核對目標再取得授權。
4. 回填或同步記錄每個範圍的實際寫入及後處理結果；不要因 API 最後回傳失敗就假定所有寫入回滾。
5. 用相容版本的真實資料庫驗證重要 NULL、精度、原子性與競態，不以 mock 代替鎖定證據。
