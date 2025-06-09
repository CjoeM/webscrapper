import requests
import json
import time
from random import choice, uniform 



USER_AGENTS=[]
with open("/Users/sellomothemane/Desktop/Olles_Scrappers/Oless_AWS/user_agents/user_agents.json") as f:
    USER_AGENTS_FILE = json.load(f)

for user in USER_AGENTS_FILE:
    USER_AGENTS.append(user["userAgent"])


url = "https://www.pnp.co.za/pnphybris/v2/pnp-spa/products/search"

headers = {
    "Content-Type": "application/json",
    "User-Agent": choice(USER_AGENTS),
}

params = {
    "fields": "products(sponsoredProduct,onlineSalesAdId,onlineSalesExtendedAdId,code,name,brandSellerId,averageWeight,summary,price(FULL),images(DEFAULT),stock(FULL),averageRating,numberOfReviews,variantOptions,maxOrderQuantity,productDisplayBadges(DEFAULT),allowedQuantities(DEFAULT),available,quantityType,defaultQuantityOfUom,inStockIndicator,defaultUnitOfMeasure,potentialPromotions(FULL),categoryNames),facets,breadcrumbs,pagination(DEFAULT),sorts(DEFAULT),freeTextSearch,currentQuery,responseJson,seoCategoryContent,seoCategoryTitle,refinedContent,categoryDescription,keywordRedirectUrl",
    "query": ":relevance:allCategories:pnpbase",
    "pageSize": "100",
    "storeCode": "WC21",
    "lang": "en",
    "curr": "ZAR"
}




all_products=[]
page=0


while True:
    try:
        headers["User-Agent"]=choice(USER_AGENTS)
        params["currentPage"]=str(page)
        response = requests.post(url, headers=headers, params=params,timeout=10)

        if response.status_code != 200:
            print(f"[!] Status {response.status_code} on page {page}. Retrying after delay...")
            time.sleep(10)
            continue

        data = response.json()
        products = data.get("products", [])
        # print(products)
        if not products:
            print(f"[✓] No more products found on page {page}.")
            break

        all_products.extend(products)
        print(f"[+] Fetched {len(products)} products from page {page} (total so far: {len(all_products)})")

        page += 1

        # Respectful scraping: wait 1–3 seconds randomly
        time.sleep(uniform(5, 10))
    except Exception as e:
        print(f"[ERROR] Exception on page {page}: {e}")
        time.sleep(5)

    print( (data.get("products", [])))
    with open("picknpay_items.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)


    print(f"\n[✓] Scraping complete. Total items: {len(all_products)}")
        # for product in products:
        #     print({
        #         # "name": product.get("name"),
        #         "price": product.get("price", {}).get("formattedValue")
        #         # "code": product.get("code"),
        #         # "brand": product.get("brandSellerId"),
        #         # "image": product.get("images", [{}])[0].get("url"),
        #         # "summary": product.get("summary"),
        #     })
        #     break
