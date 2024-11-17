from colorlog_config import logger
from db.main import get_session_local
from db.models import Car, AvailableAttribute, CarAttribute
import os
from dotenv import load_dotenv
load_dotenv()
mode = os.getenv('MODE', 'PROD')

class GeneralPipeline:
    def open_spider(self, spider):
        if spider.name == 'general':
            self.session = get_session_local()
            
    def close_spider(self, spider):
        if spider.name == 'general':
            self.session.close()
        
    def process_item(self, item, spider):
        if spider.name != 'general':
            return item
        else:
            if mode == 'DEV':
                try:
                    plate_number_seed = AvailableAttribute(id = 33924, title='차량번호', title_ru='номер машины', att_type='ATTRIBUTE', parent_att=None, description=None, ordering=None)
                    transmission_seed = AvailableAttribute(id = 33925, title='Transmission', title_ru='передача инфекции', att_type='ATTRIBUTE', parent_att=None, description=None, ordering=None)
                    
                    self.session.add(plate_number_seed)
                    self.session.add(transmission_seed)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
            try:
                car = Car()
                
                # car table
                car.car_id = item["car_id"]
                car.title = item["title"]
                car.distance = item["distance"]
                car.production_year = item["year"]
                car.price = item["price"]
                car.ready = False
                car.sold = False
                
                # car table (change in next pipeline)
                car.fuel_type = "unknown"
                car.v_type = "unknown"
                
                self.session.add(car)
                self.session.commit()
                logger.info(f"General info item for car ID {item['car_id']} added to the database.")
                
                # attributes
                
                # --- Brand ---
                brand = self._get_or_create_attribute("BRAND", item.get("brand"))
                if brand:
                    self._add_car_attribute(car.id, brand.id, 1)
                    
                # --- Model ---
                model = self._get_or_create_attribute("MODEL", item.get("model"), parent_id=brand.id if brand else None)
                if model:
                    self._add_car_attribute(car.id, model.id, 1)
                    
                # --- Submodel ---
                submodel = self._get_or_create_attribute("SUBMODEL", item.get("submodel"), parent_id=model.id if model else None) 
                if submodel:
                    self._add_car_attribute(car.id, submodel.id, 1)
                    
                # --- Grade ---
                grade = self._get_or_create_attribute("DETAILED_GRADE", item.get("grade"), parent_id=submodel.id if submodel else None)
                if grade:
                    self._add_car_attribute(car.id, grade.id, 1)
                    
                logger.info(f"Attributes for car ID {item['car_id']} added to the database.")
                    
                # TODO: add plate_number and transmission in next spider
                
                return item                
            except Exception as e:
                self.session.rollback()
                logger.critical(f"Error while adding car to the database: {e}")
    
    def _get_or_create_attribute(self, att_type, title, parent_id=None):
        if not title:
            return None

        attribute = (
            self.session.query(AvailableAttribute)
            .filter_by(title=title, att_type=att_type, parent_att=parent_id)
            .first()
        )

        if not attribute:
            attribute = AvailableAttribute(
                title=title,
                title_ru=None,
                att_type=att_type,
                parent_att=parent_id,
                description=None,
                ordering=None
            )
            self.session.add(attribute)
            self.session.commit()
        
        return attribute
    
    def _add_car_attribute(self, car_id, attribute_id, value):
        if value:
            existing_attribute = (
                self.session.query(CarAttribute)
                .filter_by(car_id=car_id, attribute_id=attribute_id)
                .first()
            )

            if not existing_attribute:
                car_attribute = CarAttribute(
                    car_id=car_id,
                    attribute_id=attribute_id,
                    value=value
                )
                self.session.add(car_attribute)
                self.session.commit()