# 更新說明（給之後接手的 Claude 看）

這個 repo 是「7-11 精品快閃購營業額看板」的公開網頁版：
https://zoe8788.github.io/711-flash-sales/

同一份看板在 Claude 裡也有一份（Dashboard 型 Artifact）：
https://claude.ai/artifact/5SLFxUE2RuQL64DWFSZZkh
兩邊要一起更新。

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
3. Claude 那份 Artifact：把同樣的 JSON 用 `upload_asset` 上傳，更新 `datasets/<id>` 的 `source.url`；
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
