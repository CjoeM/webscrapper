#!/bin/bash
echo "Starting scraper..."
python3.13.3 /scrapper/pwdemo/pnp.py
cd /scrapper/pwdemo/pwdemo/spiders
scrapy crawl pwspider -O /scrapper/pwdemo/pwdemo/spiders/pws.json