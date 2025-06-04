from scrapy import Selector
from bs4 import BeautifulSoup
import json
import re 
import pandas as pd
from datetime import datetime

pattern_size=r'\b\d+(\.\d+)?\s?(kg|g|l|m|mm|cm|ml|mg)\b'
pattern_bundle_units = r"\d+(\.\d+)?"
today=datetime.today()

with open("/Users/sellomothemane/Desktop/Olles_Scrappers/Oless_AWS/scrapper/pwdemo/json_files/asdasdasd.json", "r") as f:
    data = json.load(f)
    
data=(data[0]["product_section_html"])
# print(data)

items={"item_ID":[],"store":[],"item_name":[],"link":[],"item_size":[],"price":[],"special price":[],"brand":[],"category":[],"special":[],"special end date":[],\
       "special start date":[],"availability":[],"reward card":[],"bundle deal":[],"bundle prices":[],"bundle units":[],"date_ingested":[]}
codes_id=[]
soup = BeautifulSoup(data, "html.parser")
search_items=soup.find("div", class_="hidden productListJSON")
item_with_codes = json.loads(search_items.text.strip())
data_items = soup.find_all("div", attrs={"data-product-ga": True})
product_links = soup.find_all("div", class_="item-product__image __image")
for code in item_with_codes:
    codes_id.append(code["code"])
# print(search_items)



# soup=BeautifulSoup(data_items[10], "html.parser")

for code in codes_id:
    count=0
    links=0
    link_tag = product_links[links].find("a")
    if link_tag and link_tag.has_attr("href"):
        items["link"].append("www.checkers.co.za"+link_tag["href"])
    links=links+1
    main_items=soup.find("div",class_=f'product-frame product-ga product_{code} js-heavy-attributes-populated')


    main_items_attr = main_items.get("data-product-ga")
    data = json.loads(main_items_attr)
    # print(main_items_attr)
    items["store"].append("checkers")
    items["item_ID"].append(data["id"])
    items["item_name"].append(data["name"])
    items["price"].append("R"+data["price"])
    items["brand"].append(data["brand"])
    items["category"].append(data["category"])
    items["availability"].append(data["stock"])
    items["special start date"].append("")
    items["date_ingested"].append(today)
    size=data["name"].split(" ")
    
    for i in size:
        if re.match(pattern_size, i,re.IGNORECASE):
            count=count+1
            items["item_size"].append(i)
        
    if count==0:
        items["item_size"].append("")
    # item_caption=(main_items.find('figcaption', class_="item-product__caption"))
    item_now_price=(main_items.find('span', class_="now").contents[0].strip())
    # item_now_price=json.loads(item_now_price)
    # print(item_now_price+".99","   asdasdasdasd")
    special_valid_date=main_items.find('span', class_="item-product__valid").contents
    if len(special_valid_date)>0:
        items["special end date"].append(special_valid_date[0].split("\n")[1])
        items["special"].append("yes")
        items["special price"].append(item_now_price+".99")
        # print(main_items.find('span', class_="item-product__message__text").contents)
        try:
            
            items["reward card"].append(main_items.find('span', class_="special-price__extra__text").contents[0].split("\n ")[1])
           
            # items["description"].append("s")
            # print(items["description"])
        except:
             items["reward card"].append("")
            # items["description"].append(main_items.find('span', class_="item-product__message__text").contents)
        try:
            
            items["bundle deal"].append(main_items.find('span', class_="item-product__message__text").contents[0].split("\n ")[1])
            pattern=r'R\s?\d+'
            bundle_items=main_items.find('span', class_="item-product__message__text").contents[0].split("\n ")[1].split(" ")
            for item in bundle_items:
                if re.match(pattern, item, re.IGNORECASE):
                    items["bundle prices"].append(item)
                    for item in bundle_items:
                                if re.match(pattern_bundle_units, item, re.IGNORECASE):
                                    items["bundle units"].append(item)
                if item=="Deal":
                     items["bundle prices"].append("")
                     items["bundle units"].append("")
                
            # items["description"].append("s")
            # print(items["description"])
        except:
             items["bundle deal"].append("")
             items["bundle prices"].append("")
             items["bundle units"].append("")

            # items["description"].append(main_items.find('span', class_="item-product__message__text").contents)
        
    else:
        items["special end date"].append("")
        items["special"].append("no")
        items["special price"].append("")
        items["reward card"].append("")
        items["bundle deal"].append("")
        items["bundle prices"].append(" ")
        items["bundle units"].append("")
    # print(main_items.find('span', class_="item-product__message__text"))
    # print(main_items.find('span', class_="special-price__extra__text"))
    # print(items["description"].append(main_items.find('span', class_="item-product__message__text").contents))



# print("availanility: ", len(items["availability"]))
# print( "brand: ", len(items["brand"]))
# print("bundle deal",len(items["bundle deal"]))
# print("category ",len(items["category"]))
# print("itesm id ", len(items["item_ID"]))
# print("iteam name ",len(items["item_name"]))
# print("item size ",len(items["item_size"]))
# print("item price ",len(items["price"]))
# print("reward card ",len(items["reward card"]))
# print("special end date: ",len(items["special end date"]))
# print("special price ",len(items["special price"]))
# print("special: ",len(items["special"]))
# print("bundle prices: ", len(items["bundle prices"]))

df = pd.DataFrame(items)
df.to_json("Oless_AWS/scrapper/pwdemo/json_files/aws_json_files/checkers.json", orient="records", indent=2)
print(df)
# print(items["link"])

       
            

# for item in data_items:
#    pass

# product_list = json.loads(json_data)
# print(product_list)

# Example: Extract all product divs inside the main section
# products = selector.css('div.product__listing product__grid')  # or adjust based on the actual item class
# results=[]
