import json
import re 
import pandas as pd

pattern_size=r'\b\d+(\.\d+)?\s?(kg|g|l|m|mm|cm|ml|mg)\b'
pattern=r'R\s?\d+'
pattern_bundle_units = r"\d+(\.\d+)?"

items={"item_ID":[],"store":[],"item_name":[],"item_size":[],"price":[],"special price":[],"brand":[],"category":[],"special":[],\
       "special end date":[],"availability":[],"reward card":[],"bundle deal":[],"bundle prices":[],"bundle unites":[]}
with open("/Users/sellomothemane/Desktop/Olles_Scrappers/Oless_AWS/scrapper/pwdemo/json files/picknpay_items.json", "r") as f:
    data = json.load(f)


for item in data:
    count=0
    items["item_ID"].append(item["code"])
    items["store"].append("picknpay")
    items["item_name"].append(item["name"])
    size=item["name"].split(" ")
    for i in size:
        if re.match(pattern_size, i,re.IGNORECASE):
            count=count+1
            items["item_size"].append(i)
    if count==0:
        items["item_size"].append("")
    if item["inStockIndicator"]==True:
        items["availability"].append(1)
    else:
        items["availability"].append(0)
    items["brand"].append(item["brandSellerId"])
    items["price"].append(item["price"]["oldPriceFormattedValue"])
    items["special price"].append(item["price"]["formattedValue"])
    if item["price"]["savings"]==0:
        items["special"].append("no")
    else:   
        items["special"].append("yes")
    try:
        items["special end date"].append(item["potentialPromotions"][0]["endDate"])
        items["special"][-1]="yes"
        message=item["potentialPromotions"]["promotionTextMessage"].split(" ")
        if message[0] in range(1,99) and "Smart Price" not in item["potentialPromotions"]["promotionTextMessage"]:
            items["bundle deal"].append(item["potentialPromotions"]["promotionTextMessage"])
            items["bundle prices"].append(message[2])
            items["bundle unites"].append(message[0])
        if "Smart Price" in message:
            pass
    except:
     items["special end date"].append("")


print("item_ID: ",len(items["item_ID"]))
print("item_ID: ",len(items["store"]))
print("item_name: ",len(items["item_name"]))
print("item_size: ",len(items["item_size"]))
print("availability: ",len(items["availability"]))
print("price: ",len(items["price"]))
print("brand: ",len(items["brand"]))
print("special price: ", len(items["special price"]))
print("special: ", len(items["special"]))
print("special end date: ", len(items["special end date"]))
print("bundle deal: ", len(items["bundle deal"]))
print("bundle prices: ", len(items["bundle prices"]))
print("bundle unites: ", len(items["bundle unites"]))
print("reward card: ", len(items["reward card"]))
print("category: ", len(items["category"]))
print(items["special end date"])