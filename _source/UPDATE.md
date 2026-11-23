# 更新說明（給之後接手的 Claude 看）

這個 repo 是「7-11 精品快閃購營業額看板」的公開網頁版：
https://zoe8788.github.io/711-flash-sales/

使用者決定（2026-11-16）：**之後只更新這個 GitHub 網址**。
Claude 裡另有一份舊的 Dashboard Artifact（https://claude.ai/artifact/5SLFxUE2RuQL64DWFSZZkh），已停止同步，停在 11/8 的資料，不用再更新。

## 檔案

| 檔案 | 內容 |
|---|---|
| `_source/page.html` | 看板頁面本體（Artifact 的 `files/index.html`，同一份） |
| `_source/data/flash_sales_campaigns.json` | 檔期：id、名稱、快閃購起訖、集點起訖（`points_start`/`points_end`）、統計截止日（`asof`）、備註 |
| `_source/data/flash_sales_products.json` | 每檔每項商品：分類、下單量、銷售數、營業額、是否追加 |
| `_source/data/flash_sales_prodimg.json` | 從 DM 裁出的商品圖（base64）＋ DM 售價 |
| `_source/data/flash_sales_dm.json` | 各檔 DM 整張圖（base64），`page` 是第幾張 |
| `_source/build.py` | 從上面這些產生網頁（根目錄的 index.html、data/、img/、dm/） |

## 更新流程

1. 改 `_source/data/` 裡的 JSON（或 `page.html`）。
2. 在 repo 根目錄跑 `python3 _source/build.py`，再 commit、push 到 main。GitHub Pages 約 1 分鐘生效。
3. （已停用）Claude 那份 Artifact：把同樣的 JSON 用 `upload_asset` 上傳，更新 `datasets/<id>` 的 `source.url`；
   頁面改動則寫進 `files/index.html`。dataset id 對應：
   `campaigns`、`products`、`prodimg`、`dmimg`。

## 資料規則（使用者確認過的）

- **營業額＝成本價未稅 × 1.05 × 銷售數**（含稅）。表上只有未稅小計時乘 1.05。
- **不放成本價**：資料檔裡不存成本，頁面也不顯示。
- 銷售數用使用者表單上「用來算營業額的那一欄」（例如 2026 檔期用 2/23，不是 2/24），並在檔期設 `asof`。
- 下單量＝7-11 訂貨量＋7-11 追加；有追加或華漫加訂的商品 `added: true`。
- 沒有下單量的檔期 `ordered: null`，頁面會自動改用銷售數。
- 日期以活動 DM／海報為準；集點期只有部分檔期有。
- 米飛寫「米飛」，不是「米菲」。
- 網址是公開的：只放營業額、下單量、銷售數，不放成本。

## 每週銷售追蹤（2026-11-18 起）

- 檔期設 `weeks`：每週統計截止日清單（例：["2026-11-08","2026-11-15"]）。
- 每項商品設 `weekly_cum`：{截止日: 累計銷量}。每週新資料就加一個日期進去，`sold` 同步改成最新累計。
- 頁面會自動算每週銷量／營業額（成本價含稅）、比上週（用日均比，因為週天數不同）、檔期營業額預估（保守＝依週衰退、上限＝維持最近一週速度，皆不超過剩餘下單量），以及有追加 vs 未追加的售出率。
- 目前只有 2026 米飛暖心選物特輯（miffy-2611）有每週資料。

## 入倉量（待補貨）

- 使用者會在這份 Google 試算表更新確定的入倉量：https://docs.google.com/spreadsheets/d/1Ov18OhVqxrKlZhrOWgc6DF-1gYoG4wvT-vA6jou86Dg/edit?gid=0#gid=0
- 用「入倉數量」分頁的「已出貨」欄，寫進商品的 `stock_in`；檔期設 `stock_asof`。
- 待補貨＝累計銷量 − 已入倉（只顯示正數）。沒有 stock_in 的檔期，表格自動隱藏這一欄。

## 到貨進度（2026-11-23 起，目前只有 PINGU）

- 檔期設 `arrivals`：[{no, product, dm_price, qty, date, state, eta, eta_note}]（eta＝預計到貨日，來自商品會議記錄；`eta_asof` 為時程表日期；eta 在開賣日當天或之後會標「晚於開賣」），`arrivals_asof` 為更新日，`arrivals_note` 為補充說明。
- 頁面在檔期卡片下方顯示「到貨進度」表；有 `date` 即算已到貨。資料來源是使用者給的到貨表（xlsx），不從 ERP 抓。
- 萌蛙匹克延期，id 改為 `frog-2702`，2027/2/17 開始，結束日未定（`end` 留空）。
