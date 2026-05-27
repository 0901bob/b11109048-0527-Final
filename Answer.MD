# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11109048  
**系級：** 資管系大四
**姓名：** 陸昱暐 

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|

| Q1 l1 (in load_proc) | 讀取檔案後的所有資料行列表 | `raw_lines`, `file_lines` |
| Q2 d2 (in main) | 全部書籍資料的全域列表，包含書名、ISBN、狀態 | `books`, `book_records` |
| Q3 c_res (in check) | 檢查指定 ISBN 是否已存在於資料庫中 | `isbn_exists`, `has_isbn` |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：** 變數命名不具描述性，例如 `l1`, `d2`, `c_res`, `p`, `p2`, `t`, `i`, `s`。這讓程式邏輯難以理解與維護。
- **Q2：** 直接使用全域變數 `d2` 儲存資料，導致資料不封裝、函式依賴隱藏狀態，難以測試與重構。
- **Q3：** 使用自定義字串分割格式 `@@` 與 `##` 存取資料，格式脆弱且極易因輸入包含分隔字元而毀掉資料。
- **Q4：** 檔案讀寫缺乏錯誤處理，對 `lib_data.txt` 不存在或內容錯誤情況沒有防護，使用者輸入也沒有完整驗證。
- **Q5：** 指令解析邏輯混亂，`borrow` 操作沒有處理找不到 ISBN 的情況，`add` 也只判斷格式長度而非資料合法性。

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A：請幫我重構這個 `legacy_lib.py`，把資料儲存改成 `books.json`，並將功能拆成類別或函式，避免使用 `@@` / `##` 的自訂分割格式。

Prompt B：請整理 `add`、`show`、`borrow`、`exit` 指令的邏輯，並加上錯誤處理：檢查 `add` 格式是否正確、borrow 找不到 ISBN 要回傳 `ISBN Not Found`。

Prompt C：請修改檔案讀取與寫入程序，使用標準 JSON 結構存取書籍資料，並確保 `books.json` 無法解析時不會當機。
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？

- 有，AI 初版重構時沒有處理 `borrow` 找不到 ISBN 的情況，並且原始 `add` 格式驗證不夠完整。我發現這些問題時是閱讀程式碼並在測試時手動檢查邏輯輸入後發現的。

2. 發現的問題：

- AI 漏掉了 `borrow` 指令找不到 ISBN 時的回應。
- 初版沒辦法正確處理空白或格式錯誤的 `add` 輸入。
- 初版 `books.json` 讀取缺少錯誤保護，空檔案或不合法 JSON 會造成例外。

3. 修正的對話：

- 我告訴它「請在 `borrow` 找不到書籍時印出 `ISBN Not Found`，不要直接跳過。」
- 我也提示它「`add` 需要三個欄位，格式錯誤時要回覆 `Format Error`。」
- 最後我補充「讀取 `books.json` 要用標準 JSON，不合法時要以空資料庫啟動並顯示警告。」

---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
=== 圖書管理系統 v1.0 (Modern) ===
> Success
> 書名: Book One, ISBN: 12345, 狀態: available
> Updated
> 書名: Book One, ISBN: 12345, 狀態: borrowed
> 系統關閉
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
    {
        "title": "Book One",
        "isbn": "12345",
        "status": "borrowed"
    }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
# 請在此處貼上 git log 內容
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
# 請貼上你的 Repo 網址
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
