import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List,Dict
from bs4 import BeautifulSoup
import uuid
import re
from urllib.parse import urlparse, parse_qs

class AmericanTourister(scrapy.Spider):
    name = 'american_tourister_dac'
    brand_name = 'AMERICAN_TOURISTER'
    spider_type: str = 'chain'
    spider_chain_id = "23930"
    spider_categories: List[str] = [Code.SHOPPING_MALL]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ["www.americantourister.in"]
    start_urls = ['https://www.americantourister.in/index.php?route=extension/module/wk_store_locater/setter']
    def start_requests(self):
        headers = {
            'User-Agent': 'PostmanRuntime/7.32.3',
        }

        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Extract the data as a single string and split it using '~' as the delimiter for different records
        data = response.text.split('~')

        for record in data:
            # Split the record using '!' as the delimiter
            record_values = record.split('!')

            if len(record_values) == 17:
                store_id = record_values[0]
                latitude = float(record_values[1])
                longitude = float(record_values[2])
                store_name = record_values[3]
                address = record_values[4]
                city = store_name.split()[-1]
                phone_number = record_values[12]
                opening_hours = record_values[13]

            data = {
                'ref': uuid.uuid4().hex,
                'chain_id': '23930',
                'chain_name': 'AMERICAN_TOURISTER',
                'addr_full':address,
                'name' :store_name, 
                'phone':phone_number,
                'opening_hours':opening_hours,
                'website': 'https://www.americantourister.in/index.php?route=extension/module/wk_store_locater/setter',
                'lon':longitude,
                'lat':latitude,
                'brand':'AMERICAN_TOURISTER',
                'city' : city,
                'country': 'India'
                

            }

            yield GeojsonPointItem(**data)

    