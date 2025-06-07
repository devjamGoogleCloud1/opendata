import json

# 輸入和輸出檔案名稱
input_file = "臺北市公園基本資料.json"
output_file = "park_utf8.json"

# 讀取原始 JSON（可能含有 unicode 編碼）
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 重新寫入 JSON，確保中文字正確顯示（不轉為 \uXXXX）
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"已轉換完成：{output_file}")
