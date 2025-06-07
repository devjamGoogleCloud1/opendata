import json

with open('all_rent.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

filtered_data = [item for item in data if item.get("address")]

with open('all_rent.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f"已刪除 address 為空的項目，剩餘 {len(filtered_data)} 筆資料。")
