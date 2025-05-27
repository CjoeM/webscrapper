import scrapy
import json
from scrapy_playwright.page import PageMethod


class PwspiderSpider(scrapy.Spider):
    name = "pwspider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.checkers.co.za/c-2256/All-Departments",
                                         meta={"playwright":True})

    def parse(self, response):
        # raw_json = response.css("div.productListJSON::text").get()
        product_section_html = response.css("div.product__listing.product__grid").get()

        # Yield the entire section HTML
        yield {
            "product_section_html": product_section_html
        }


        # for product in response.css("div.main_inner-wrapper wrap"):
        #     yield {
        #         "text": response.text
        #     }
