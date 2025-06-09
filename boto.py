import boto3
import json
import pandas as pd
import json 
from io import StringIO

shoprite="/Users/sellomothemane/Desktop/Olles_Scrappers/Oless_AWS/scrapper/pwdemo/json_files/aws_json_files/shoprite.json"
checkers="/Users/sellomothemane/Desktop/Olles_Scrappers/Oless_AWS/scrapper/pwdemo/json_files/aws_json_files/checkers.json"
picknpay="/Users/sellomothemane/Desktop/Olles_Scrappers/Oless_AWS/scrapper/pwdemo/json_files/aws_json_files/picknpay.json"
files =[shoprite,checkers,picknpay]
merged_data = []

for file in files:
    with open(file, "r") as f:
        data = json.load(f)
        merged_data.extend(data)
         

with open("/Users/sellomothemane/Desktop/Olles_Scrappers/Oless_AWS/scrapper/pwdemo/json_files/aws_json_files/collective_stores.json", "w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=2)



s3=boto3.client("s3")
bucket_name="combined_groceries"
object_name="collective_stores.json"

s3.upload_file("/Users/sellomothemane/Desktop/Olles_Scrappers/Oless_AWS/scrapper/pwdemo/json_files/aws_json_files/collective_stores.json",bucket_name,object_name)
# print(shoprite)