# 日常工作流

| 任務 | 主要入口 | 完成證據 |
| --- | --- | --- |
| 釐清需求 | 未定案時用 grill-me；to-spec 整理已討論內容；明確時直接 workflow-delivery | 可觀察驗收結果與未定政策 |
| Prototype／POC | workflow-prototype | 可操作入口、觀察結果、確認需求與未定事項 |
| 實作 | workflow-delivery + 前後端專業 skill | 改動、測試、實際流程 |
| 除錯 | workflow-debug | 重現、原因、修正前後結果 |
| 提交變更 | workflow-commit | 提交範圍、SHA、相關驗證及保留的其他工作 |
| 建立／更新 PR | workflow-create-pr | PR URL、base/head、遠端 SHA 與 CI 終態 |
| Ship PR | workflow-delivery 串接 commit 與 create-pr | 實作驗證、提交、push、PR 與 CI |
| 處理 review 回饋 | workflow-review → commit／create-pr（依授權） | 意見核實、修正驗證、遠端 SHA；回覆與 thread 狀態分開確認 |
| 自己的變更送審前自查 | workflow-review：author self-review | 完整任務 diff、修正及驗證、剩餘風險；不等於獨立核准 |
| 身為 reviewer 審查變更 | workflow-review：reviewer | 精確 head/base、嚴重度、觸發情境、影響與位置；預設唯讀 |
| 前端驗收 | workflow-browser-qa | 環境、步驟、畫面／網路證據 |
| 相依 PR | gh-stack | 每層增量、base、CI 與整體行為 |
| 交接 | workflow-delivery 的交接模板，更新原任務文件 | 已完成、未完成、SHA、下一步及已授權動作 |

需求不確定時，可由 grill-me 釐清問題，再以 [workflow-prototype](../skills/common/workflow-prototype/SKILL.md) 驗證互動、流程或狀態模型；方向確認後，視需要用 to-spec 整理，再進入 workflow-delivery。Prototype 是選用階段，既有需求明確時直接實作。原型需提供可操作入口並區分 mock 與正式行為，確認可重用想法及需重寫的部分；能展示不等於使用者已接受，也不代表可直接上線。

同一階段選一個主流程，專業 skills 補充檢查範圍。沿用已確認設計與授權，不因同時安裝多個需求或 TDD skill 重複訪談。只有影響行為的未知政策才詢問使用者。

需求角度看是否解決原問題；架構看邊界；工程看實作；QA 看失敗路徑與證據；使用者看操作是否清楚。一般任務按風險選角度，使用者要求獨立多角色 review 時才分派獨立 agent。

開工讀規則與 Git 狀態，保留無關修改，以最小可驗證範圍實作。使用者要求 commit／push／PR 時完成操作，檢查精確 commit 的 CI，再回報成果。對外留言、merge 與破壞性資料操作維持在授權範圍。

commit／PR 格式優先採用使用者本次要求，再採用 repo 規範；未指定時使用 skills 內的預設模板。PR 一律以 ELI20 說明：讓具基本軟體常識、未參與開發的 reviewer 看懂問題、修改後行為、必要取捨與驗證結果。repo 已有 template 時保留欄位，內容仍採 ELI20。

截圖、unit test、真實 DB 測試、CI 與使用者驗收分別回答不同問題，不互相替代。

Matt Pocock 工程 skills 第一次用在某專案前，先執行 `setup-matt-pocock-skills` 確認該專案的 issue tracker 與文件位置。`to-spec` 整理已討論的內容，不代替需求訪談；只有已授權發佈時才寫到外部 tracker。需要精簡回覆時使用 `caveman`，它不改變工作範圍或繁體中文偏好。

交付前先依風險自查完整任務 diff：驗收結果、修改範圍、受影響呼叫端、失敗路徑及驗證是否支持成果。文件修改檢查內容與連結即可；不強制每次安排獨立 agent。

收到 review 回饋後，先核對目前 head、意見與實際程式，再修正已確認的問題；政策未定時一次確認一項。有授權才提交、更新 PR、回覆或 resolve thread，並分開確認修正、遠端 CI 與討論狀態。

跨 session 使用 [交接模板](../skills/common/workflow-delivery/templates/handoff.md)，更新原任務文件的現況；沒有任務文件時先在對話交接。記錄目標、branch／SHA、未提交修改、驗證、下一步及授權，不另建歷史日誌。接手時重新核對 Git 與相關遠端狀態，舊測試結果只代表其記錄的版本與環境。

Review 依任務角色分流：自己的變更可在已授權範圍內自查、修正並接續交付；身為 reviewer 時先提供 findings，不自行改作者分支。收到別人對自己 PR 的意見則走回饋處理流程。發佈 review、approve／request changes、回覆與 resolve thread 均依相應授權。

提交與 push 前重新核對目標 branch、PR head／base 與 remote，避免共用 checkout 中途切換分支。新增元件、hook 或工具函式前先搜尋既有實作。版本、schema 與 domain 定義等判斷提供可追溯證據；CI-only 失敗先讀該版本 log、比較環境並嘗試重現，不靠猜測性 push 反覆試錯。分支切換不會重設資料庫，排查 schema 錯誤時需核對 migration 狀態。

Skills 保持精簡：description 只說明明確用途，本文保留影響判斷的慣例、邊界與完成條件；模板需要時才讀。依任務選擇相關文件與驗證，必要檢查通過後，只有新變更、失敗或未解疑慮才擴大或重跑。已授權工作持續做到完成，不因切換 skill 重複要求確認。

DDD、CQRS、Hexagonal Architecture 與 BDD 是[按需選用的 skills](../skills/README.md#按需選用)，不屬於必跑階段。釐清行為時可用 BDD 補充具體例子；設計或維護相關架構時才載入對應 skill。一般任務維持既有架構，選用一項不代表連帶採用其他模式。
