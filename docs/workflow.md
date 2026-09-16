# 日常工作流

| 任務 | 主要入口 | 完成證據 |
| --- | --- | --- |
| 釐清需求 | 未定案時選 ito-grill／ito-prd；明確時直接 workflow-delivery | 可觀察驗收結果與未定政策 |
| 實作 | workflow-delivery + 前後端專業 skill | 改動、測試、實際流程 |
| 除錯 | workflow-debug | 重現、原因、修正前後結果 |
| PR review | workflow-review | 精確 head/base、觸發情境、影響與位置 |
| 前端驗收 | workflow-browser-qa | 環境、步驟、畫面／網路證據 |
| 相依 PR | gh-stack | 每層增量、base、CI 與整體行為 |
| 交接 | 原任務文件 | 已完成、未完成、SHA、下一步及已授權動作 |

同一階段選一個主流程，專業 skills 補充檢查範圍。沿用已確認設計與授權，不因同時安裝多個需求或 TDD skill 重複訪談。只有影響行為的未知政策才詢問使用者。

需求角度看是否解決原問題；架構看邊界；工程看實作；QA 看失敗路徑與證據；使用者看操作是否清楚。一般任務按風險選角度，使用者要求獨立多角色 review 時才分派獨立 agent。

開工讀規則與 Git 狀態，保留無關修改，以最小可驗證範圍實作。使用者要求 commit／push／PR 時完成操作，檢查精確 commit 的 CI，再回報成果。對外留言、merge 與破壞性資料操作維持在授權範圍。

截圖、unit test、真實 DB 測試、CI 與使用者驗收分別回答不同問題，不互相替代。
