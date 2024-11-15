import scrapy
import json
from colorlog_config import logger
from getcha.constants import car_list_headers
from getcha.items import GeneralInfoItem

class GeneralSpider(scrapy.Spider):
    name = "general"
    allowed_domains = ["m.getcha.kr", "api.getcha.io"]

    car_list_url = 'https://api.getcha.io/api/used-car/sale/filter?page=1&sort=relevant&direction=desc'
    
    def start_requests(self):
        payload = {
            "conditions": [
                {"type": "PRICE", "min": 0, "max": 20000},
                {"type": "MILEAGE", "min": 0, "max": 200000},
                {"type": "MODEL_YEAR", "min": 2010, "max": 2024, "label": "전체"},
                {"type": "FUEL", "list": []},
                {"type": "DRIVING_SYSTEM", "list": []},
                {"type": "COLOR", "list": []},
                {"type": "ACCIDENT_FREE", "option": None}
            ],
            "type": "AND"
        }
        
        yield scrapy.Request(
            url=self.car_list_url, 
            method='POST', 
            body=json.dumps(payload), 
            headers=car_list_headers,
            callback=self.parse, 
        )

    def parse(self, response):
        if response.status == 200:
            logger.info("Data retrieved successfully. Status code: %s", response.status)
        else:
            logger.error("Failed to retrieve data. Status code: %s", response.status)
            

        data = response.json()["result"]["data"]
        
        for car in data:
            model_parts = car["modelName"].split()
            brand = model_parts[0] if len(model_parts) > 0 else ""
            model = model_parts[1] if len(model_parts) > 1 else ""
            submodel = " ".join(model_parts[2:]) if len(model_parts) > 2 else ""
            
            item = GeneralInfoItem()
            item["car_id"] = car["id"]
            item["title"] = car["modelName"]
            item["distance"] = car["mileage"]
            item["year"] = car["carYear"]
            item["price"] = car["price"]
            item["brand"] = brand
            item["model"] = model
            item["submodel"] = submodel
            item["grade"] = submodel
            
            logger.info(f"General info item for car ID {car['id']}: {item}")
            yield item