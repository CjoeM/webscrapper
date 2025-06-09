import scrapy
import random
import asyncio
from scrapy_playwright.page import PageMethod

class PwSpider(scrapy.Spider):
    name = "pwspider"
    allowed_domains = ["shoprite.co.za","products.checkers.co.za"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.shoprite.co.za/c-2413/All-Departments/Food?q=%3Arelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page=0",
            headers={
                "accept-language": random.choice(["en-US,en;q=0.9", "en-ZA,en;q=0.8"]),
            },
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_timeout", 2000),
                    PageMethod("wait_for_selector", "div.product__listing.product__grid"),
                ],
                "playwright_context_kwargs": {
                    "user_agent": random.choice(self.settings.get("USER_AGENTS")),
                    "viewport": {"width": random.choice([1280, 1366, 1920]), "height": random.choice([720, 768, 1080])},
                    "locale": random.choice(["en-US", "en-ZA"]),
                },
                "proxy": random.choice(self.settings.get("PROXIES", [None])),
                "page_number": 0,
            },
            callback=self.parse
        )

    async def parse(self, response):
        page = response.meta["page_number"]
        
        product_section_html = response.css("div.product__listing.product__grid").get()

        if not product_section_html:
            self.logger.info(f"No products found on page {page}. Stopping crawl.")
            return

        yield {
            f"product_section_html": product_section_html
        }

        # Random pause: 2–4 minutes
        if page % 3 == 0:
            pause = random.randint(30, 90)
            self.logger.info(f"Pausing for {pause} seconds before page {page + 1}...")
            await asyncio.sleep(pause)

        # Prepare next request
        next_page = page + 1
        next_url = f"https://www.shoprite.co.za/c-2413/All-Departments/Food?q=%3Arelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page=0{next_page}"

        yield scrapy.Request(
            url=next_url,
            headers={
                "accept-language": random.choice(["en-US,en;q=0.9", "en-ZA,en;q=0.8"]),
            },
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_timeout", 2000),
                    PageMethod("wait_for_selector", "div.product__listing.product__grid"),
                ],
                "playwright_context_kwargs": {
                    "user_agent": random.choice(self.settings.get("USER_AGENTS")),
                    "viewport": {"width": random.choice([1280, 1366, 1920]), "height": random.choice([720, 768, 1080])},
                    "locale": random.choice(["en-US", "en-ZA"]),
                },
                "proxy": random.choice(self.settings.get("PROXIES", [None])),
                "page_number": next_page,
            },
            callback=self.parse
        )


        # for product in response.css("div.main_inner-wrapper wrap"):
        #     yield {
        #         "text": response.text
        #     }




# import scrapy
# import json
# from scrapy_playwright.page import PageMethod


# class PwspiderSpider(scrapy.Spider):
#     name = "pwspider"

#     def start_requests(self):
#         yield scrapy.Request(url="https://www.shoprite.co.za/c-2413/All-Departments/Food",
#                                          meta={"playwright":True})
        
        

#     def parse(self, response):
#         # raw_json = response.css("div.productListJSON::text").get()
#         product_section_html = response.css("div.product__listing.product__grid").get()

#         # Yield the entire section HTML
#         yield {
#             "product_section_html": product_section_html
#         }


#         # for product in response.css("div.main_inner-wrapper wrap"):
#         #     yield {
#         #         "text": response.text
#         #     }
