import requests
import xml.etree.ElementTree as ET
import json
import time

area_data = {
    '台北市': [
        '中正區', '大同區', '中山區', '萬華區', '信義區', '松山區', '大安區', '南港區', '北投區', '內湖區', '士林區', '文山區'
    ]
}

def fetch_7eleven_stores(city, town):
    url = "https://emap.pcsc.com.tw/EMapSDK.aspx"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36"),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://emap.pcsc.com.tw/",
        "Origin": "https://emap.pcsc.com.tw"
    }

    data = {
        "commandid": "SearchStore",
        "city": city,
        "town": town,
        "roadname": "",
        "ID": "",
        "StoreName": "",
        "SpecialStore_Kind": "",
        "leftMenuChecked": "",
        "address": ""
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.encoding = 'utf-8'
        return parse_store_xml(response.text)
    except Exception as e:
        print(f"❌ {city} {town} 抓取錯誤: {e}")
        return []

def parse_store_xml(xml_str):
    root = ET.fromstring(xml_str)
    stores = []

    for geo in root.findall('GeoPosition'):
        stores.append({
            "id": geo.findtext("POIID", "").strip(),
            "name": geo.findtext("POIName", "").strip(),
            "tel": geo.findtext("Telno", "").strip(),
            "address": geo.findtext("Address", "").strip(),
            "px": geo.findtext("X", "").strip(),
            "py": geo.findtext("Y", "").strip()
        })

    return stores

def main():
    all_stores = []

    for city, towns in area_data.items():
        for town in towns:
            print(f"📍 抓取中：{city} {town}")
            stores = fetch_7eleven_stores(city, town)
            for s in stores:
                s["city"] = city
                s["town"] = town
            all_stores.extend(stores)

    with open("seven_store.json", "w", encoding="utf-8") as f:
        json.dump(all_stores, f, ensure_ascii=False, indent=2)

    print("✅ 抓取完成，共儲存", len(all_stores), "筆資料。")

if __name__ == "__main__":
    main()
