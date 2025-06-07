import csv
import json
import argparse

FIELD_MAP = {
    "編號": "id",
    "案類": "type",
    "發生日期": "date",
    "發生時段": "time",
    "發生地點": "address"
}

def csv_to_json(csv_path, json_path):
    with open(csv_path, mode='r', encoding='big5', errors='ignore') as csv_file:
        reader = csv.DictReader(csv_file)
        data = []
        for row in reader:
            converted = {FIELD_MAP.get(k, k): v for k, v in row.items()}
            data.append(converted)

    with open(json_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Big5 CSV to JSON with English keys")
    parser.add_argument("csv", help="Input Big5 CSV file")
    parser.add_argument("json", help="Output JSON file")
    args = parser.parse_args()

    csv_to_json(args.csv, args.json)
