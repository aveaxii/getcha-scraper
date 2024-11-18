import scrapy
import json
from colorlog_config import logger
from getcha.constants import car_detail_headers
from getcha.items import GeneralInfoItem
from getcha.spiders.base import BaseSpider

class DetailSpider(BaseSpider):
    name = "detail"
    allowed_domains = ["m.getcha.kr", "api.getcha.io"]

    detail_url = 'https://api.getcha.io/api/used-car/sale/{car_id}'
    
    def start_requests(self):

        car_ids = self.get_car_ids()
        
        for car in car_ids:
            car_url = self.detail_url.format(car_id=car.car_id)
          
            yield scrapy.Request(
              url=car_url,  
              headers=car_detail_headers,
              callback=self.parse, 
          )

    def parse(self, response):
        if response.status == 200:
            logger.info("Detail info retrieved successfully. Status code: %s", response.status)
        else:
            logger.error("Failed to retrieve data. Status code: %s", response.status)
        
        data = response.json()
        
        if isinstance(data, list):  # If JSON is a list
            self.logger.info("First 5 items in JSON response: %s", data[:5])
        elif isinstance(data, dict):  # If JSON is a dictionary
            first_five_items = dict(list(data.items())[:5])
            self.logger.info("First 5 key-value pairs in JSON response: %s", json.dumps(first_five_items, indent=2))
        else:
            self.logger.info("Response JSON is neither a list nor a dictionary.")
            

        # data = response.json()["result"]["data"]
        
        # for car in data:
        #     model_parts = car["modelName"].split()
        #     brand = model_parts[0] if len(model_parts) > 0 else ""
        #     model = model_parts[1] if len(model_parts) > 1 else ""
        #     submodel = " ".join(model_parts[2:]) if len(model_parts) > 2 else ""
            
        #     item = GeneralInfoItem()
        #     item["car_id"] = car["id"]
        #     item["title"] = car["modelName"]
        #     item["distance"] = self.clean_number(car["mileage"])
        #     item["year"] = self.format_date(car["carYear"])
        #     item["price"] = car["price"]
        #     # available attributes
        #     item["brand"] = brand
        #     item["model"] = model
        #     item["submodel"] = submodel
        #     item["grade"] = submodel
            
        #     logger.info(f"General info item for car ID {car['id']}: {item}")
        #     yield item