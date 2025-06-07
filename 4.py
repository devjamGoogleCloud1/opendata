import json

ADDRESS_KEYWORDS = ["路", "街", "巷", "道", "段"]

def is_valid_address(address):
    return any(keyword in address for keyword in ADDRESS_KEYWORDS)

with open('all_rent.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

filtered_data = [item for item in data if "address" in item and is_valid_address(item["address"])]

with open('all_rent.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f"保留包含地址關鍵字的資料，共 {len(filtered_data)} 筆。")
