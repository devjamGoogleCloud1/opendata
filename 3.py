import requests
import json
import re
import time

area_data = {
    '台北市': [
        '中正區', '大同區', '中山區', '萬華區', '信義區', '松山區', '大安區', '南港區', '北投區', '內湖區', '士林區', '文山區'
    ]
}

API_URL = "https://api.map.com.tw/net/familyShop.aspx"
API_KEY = "6F30E8BF706D653965BDE302661D1241F8BE9EBC"

headers = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/125.0.6422.60 Safari/537.36"),
    "Referer": "https://www.family.com.tw/"
}

def fetch_family(city, area):
    params = {
        "searchType": "ShopList",
        "type": "",
        "city": city,
        "area": area,
        "road": "",
        "fun": "showStoreList",
        "key": API_KEY
    }

    try:
        res = requests.get(API_URL, headers=headers, params=params, timeout=10)
        res.encoding = 'utf-8'
        raw = res.text

        # 使用正則提取陣列
        match = re.search(r"showStoreList\((\[.*?\])\);?", raw, re.DOTALL)
        if match:
            store_list = json.loads(match.group(1))
            return store_list
        else:
            print(f"⚠️ {city} {area} 無資料或格式錯誤")
            return []

    except Exception as e:
        print(f"❌ {city} {area} 抓取失敗: {e}")
        return []

def main():
    results = []

    for city, districts in area_data.items():
        for area in districts:
            print(f"📍 抓取 {city} {area}")
            stores = fetch_family(city, area)
            for s in stores:
                results.append({
                    "city": city,
                    "district": area,
                    "name": s.get("NAME", "").strip(),
                    "tel": s.get("TEL", "").strip(),
                    "address": s.get("addr", "").strip(),
                    "lon": s.get("px"),
                    "lat": s.get("py")
                })

    with open("family_store.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ 全部完成，共 {len(results)} 間店家已儲存。")

if __name__ == "__main__":
    main()
