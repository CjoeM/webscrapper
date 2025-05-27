import requests
import json

url = "https://www.pnp.co.za/pnphybris/v2/pnp-spa/products/search"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}

params = {
    "fields": "products(sponsoredProduct,onlineSalesAdId,onlineSalesExtendedAdId,code,name,brandSellerId,averageWeight,summary,price(FULL),images(DEFAULT),stock(FULL),averageRating,numberOfReviews,variantOptions,maxOrderQuantity,productDisplayBadges(DEFAULT),allowedQuantities(DEFAULT),available,quantityType,defaultQuantityOfUom,inStockIndicator,defaultUnitOfMeasure,potentialPromotions(FULL),categoryNames),facets,breadcrumbs,pagination(DEFAULT),sorts(DEFAULT),freeTextSearch,currentQuery,responseJson,seoCategoryContent,seoCategoryTitle,refinedContent,categoryDescription,keywordRedirectUrl",
    "query": ":relevance:allCategories:pnpbase",
    "pageSize": "150",
    "storeCode": "WC21",
    "lang": "en",
    "curr": "ZAR"
}

response = requests.post(url, headers=headers, params=params)
data = response.json()

#  Parse the products
products = data.get("products", [])
# print(products)

print(len(data.get("products", [])))
with open("picknpay_items.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)
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
