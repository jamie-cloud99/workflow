---
name: workflow-frontend-contracts
description: 修改前端 API schema、權限顯示、表單或 URL 狀態時使用。
---

# workflow-frontend-contracts

1. 列出 UI 實際使用的欄位及空值、錯誤、權限與狀態含義，對照真實後端合約。
2. 嚴格驗證會影響畫面、授權與計算的欄位；忽略未使用欄位，避免跨 endpoint schema 互相綁定。
3. 處理舊頁籤、重複提交、返回頁面及 URL 重載；權限或角色資料無效時不渲染正常操作。
4. 在真實入口驗證成功、拒絕、失敗重試與資料重整；清楚分開 mock 與整合驗證。
