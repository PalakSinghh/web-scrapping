# -*- coding: utf-8 -*-
import scrapy
import re
import uuid
from locations.items import GeojsonPointItem
from locations.categories import Code
from scrapy import Selector
from typing import List, Dict
import pycountry
import requests
import json

class klubfox(scrapy.Spider):
    name = 'klubfox'
    brand_name = 'Klub Fox'
    spider_type = 'chain'
    spider_chain_name = 'Klub Fox'
    spider_chain_id = 34167
    spider_categories = [Code.MENS_APPAREL]
  

    def start_requests(self):
        url: str = "https://www.klubfox.com/"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )



    def parse(self, response):
        import json

        url = "https://www.klubfox.com/_api/cloud-data/v1/wix-data/collections/query"

        payload = json.dumps({
        "collectionName": "Items",
        "dataQuery": {
            "filter": {
            "$and": []
            },
            "sort": [
            {
                "fieldName": "shortDescription",
                "order": "ASC"
            },
            {
                "fieldName": "title",
                "order": "ASC"
            }
            ],
            "paging": {
            "offset": 50,
            "limit": 100
            },
            "fields": []
        },
        "options": {},
        "includeReferencedItems": [],
        "segment": "LIVE",
        "appId": "561930a7-378c-483c-a2ec-43fbd8aaa0f5"
        })
        headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
        'authorization': 'wixcode-pub.3297c0360e7b0a5f6f826f1f76b269d050430b0e.eyJpbnN0YW5jZUlkIjoiZjBiZWViZDgtN2JmMi00OTgxLTlmMDItYTAzOTJkZDM2MjFiIiwiaHRtbFNpdGVJZCI6IjBmMGYyZmZlLTMzOTAtNDQ1OC1hMjdkLTE2ODU0OTk5ZmJiMyIsInVpZCI6bnVsbCwicGVybWlzc2lvbnMiOm51bGwsImlzVGVtcGxhdGUiOmZhbHNlLCJzaWduRGF0ZSI6MTY5MDIwMzkzMDYwNiwiYWlkIjoiZTVlYjZlN2UtYzdlYi00NWRjLWI2YzktOTMzOTYyZTM0ZDE4IiwiYXBwRGVmSWQiOiJDbG91ZFNpdGVFeHRlbnNpb24iLCJpc0FkbWluIjpmYWxzZSwibWV0YVNpdGVJZCI6IjNlODcxNDgxLThkNTItNGEyMi1iZGMwLTgwYzM1YjAzZDBlOSIsImNhY2hlIjpudWxsLCJleHBpcmF0aW9uRGF0ZSI6bnVsbCwicHJlbWl1bUFzc2V0cyI6Ikhhc0RvbWFpbixTaG93V2l4V2hpbGVMb2FkaW5nLEFkc0ZyZWUiLCJ0ZW5hbnQiOm51bGwsInNpdGVPd25lcklkIjoiNTFlOWY4ODQtZjg3Yi00ZWJhLTllY2MtNmM0YTExYTNlNTNhIiwiaW5zdGFuY2VUeXBlIjoicHViIiwic2l0ZU1lbWJlcklkIjpudWxsLCJwZXJtaXNzaW9uU2NvcGUiOm51bGx9',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.klubfox.com/_partials/wix-thunderbolt/dist/clientWorker.eff8282f.bundle.min.js',
        'commonConfig': '%7B%22brand%22%3A%22wix%22%2C%22BSI%22%3A%22ec51fed4-a0d0-4ecf-9501-55fcdf28767a%7C1%22%7D',
        'x-wix-brand': 'wix',
        'X-Wix-Client-Artifact-Id': 'wix-thunderbolt',
        'Cookie': 'XSRF-TOKEN=1690370989|QjRdRj1qyIxQ'
        }

        response1 = requests.request("POST", url, headers=headers, data=payload)
        print(response1.status_code)
        

        # url = "https://www.klubfox.com/_api/cloud-data/v1/wix-data/collections/query"
        # payload = "{\"collectionName\":\"Items\",\"dataQuery\":{\"filter\":{\"$and\":[]},\"sort\":[{\"fieldName\":\"shortDescription\",\"order\":\"ASC\"},{\"fieldName\":\"title\",\"order\":\"ASC\"}],\"paging\":{\"offset\":50,\"limit\":150},\"fields\":[]},\"options\":{},\"includeReferencedItems\":[],\"segment\":\"LIVE\",\"appId\":\"561930a7-378c-483c-a2ec-43fbd8aaa0f5\"}"
        # headers = {
        # 'authorization': 'wixcode-pub.3297c0360e7b0a5f6f826f1f76b269d050430b0e.eyJpbnN0YW5jZUlkIjoiZjBiZWViZDgtN2JmMi00OTgxLTlmMDItYTAzOTJkZDM2MjFiIiwiaHRtbFNpdGVJZCI6IjBmMGYyZmZlLTMzOTAtNDQ1OC1hMjdkLTE2ODU0OTk5ZmJiMyIsInVpZCI6bnVsbCwicGVybWlzc2lvbnMiOm51bGwsImlzVGVtcGxhdGUiOmZhbHNlLCJzaWduRGF0ZSI6MTY5MDIwMzkzMDYwNiwiYWlkIjoiZTVlYjZlN2UtYzdlYi00NWRjLWI2YzktOTMzOTYyZTM0ZDE4IiwiYXBwRGVmSWQiOiJDbG91ZFNpdGVFeHRlbnNpb24iLCJpc0FkbWluIjpmYWxzZSwibWV0YVNpdGVJZCI6IjNlODcxNDgxLThkNTItNGEyMi1iZGMwLTgwYzM1YjAzZDBlOSIsImNhY2hlIjpudWxsLCJleHBpcmF0aW9uRGF0ZSI6bnVsbCwicHJlbWl1bUFzc2V0cyI6Ikhhc0RvbWFpbixTaG93V2l4V2hpbGVMb2FkaW5nLEFkc0ZyZWUiLCJ0ZW5hbnQiOm51bGwsInNpdGVPd25lcklkIjoiNTFlOWY4ODQtZjg3Yi00ZWJhLTllY2MtNmM0YTExYTNlNTNhIiwiaW5zdGFuY2VUeXBlIjoicHViIiwic2l0ZU1lbWJlcklkIjpudWxsLCJwZXJtaXNzaW9uU2NvcGUiOm51bGx9',
        # 'Content-Type': 'text/plain',
        # 'Cookie': 'XSRF-TOKEN=1690206025|2jcAtm_nkuG2'
        # }
        # response1 = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)
        data = response1.json()
        
        stores = data["items"]
        for row in stores:
            store = {
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                "ref": uuid.uuid4().hex,
                "addr_full": row.get('longDescription'),
                "website" :url
                # "Owner": row.get('_owner'),
                # "state": row.get('title'),
            }
            yield GeojsonPointItem(**store)