# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GeneralInfoItem(scrapy.Item):
    # car table
    car_id = scrapy.Field()
    title = scrapy.Field()
    distance = scrapy.Field()
    year = scrapy.Field()
    price = scrapy.Field()
    # avail attr and car attr
    brand = scrapy.Field()
    model = scrapy.Field()
    submodel = scrapy.Field()
    grade = scrapy.Field()
    
class DetailInfoItem(scrapy.Item):
    # car table
    color = scrapy.Field()
    fuel_type = scrapy.Field()
    reg_date = scrapy.Field()
    # avail attr and car attr
    plate_number = scrapy.Field()
    transmission = scrapy.Field()

