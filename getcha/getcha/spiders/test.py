import scrapy
import json
from colorlog_config import logger
from getcha.constants import car_list_headers

class TestSpider(scrapy.Spider):
    name = "test"
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
            
            
        