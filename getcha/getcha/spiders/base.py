from datetime import datetime
import scrapy
from db.main import get_session_local
from colorlog_config import logger
import os
from contextlib import contextmanager
from db.models import Metadata, Car
import json

class BaseSpider(scrapy.Spider):
  @contextmanager
  def get_session(self):
    session = get_session_local()
    try:
      yield session
    except Exception as e:
      session.rollback()
      logger.error(f"Transaction error: {e}")
    finally:
      session.close()
      
  def clean_number(self, number):
    if isinstance(number, str):
      return number.replace(",", "").replace("km", "")
    else:
      return number
    
  def format_date(self, date_str):
    if isinstance(date_str, str):
      return "20" +date_str.split("년")[0]
    else:
      return date_str
  
  def get_active_cookies(self):
    try:
      with self.get_session() as session:
        metadata = session.query(Metadata).order_by(Metadata.id.desc()).first()
        cookies = json.loads(metadata.cookies) if isinstance(metadata.cookies, str) else metadata.cookies
        return cookies
    except Exception as e:
      logger.error(f"Failed to get active cookies: {e}")
      return None
    
  def get_total_cars(self):
    try:
      with self.get_session() as session:
        metadata = session.query(Metadata).order_by(Metadata.id.desc()).first()
        total_cars = str(metadata.total_cars)
        formatted_total_cars = self.clean_number(total_cars)
        return formatted_total_cars
    except Exception as e:
      logger.error(f"Failed to get total cars: {e}")
      return None
    
  def format_cookies_for_curl(self, cookies_dict):
      return "; ".join([f"{key}={value}" for key, value in cookies_dict.items()])
    
  def parse_cookies_string(self, cookies):
      if isinstance(cookies, dict):
          return cookies
      
      cookies_dict = {}
      for cookie in cookies.split("; "):
          key, value = cookie.split("=", 1)
          cookies_dict[key] = value
      return cookies_dict
    
  def parse_registration_date(self, date_str):
    date_str = date_str.replace("오전", "AM").replace("오후", "PM")
    
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d %p %I:%M:%S")
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.error(f"Failed to parse date: {date_str}")
        return None
      
  def get_car_ids(self):
    try:
      with self.get_session() as session:
        car_ids = session.query(Car.car_id).all()
        return car_ids
    except Exception as e:
      logger.error(f"Failed to get car ids: {e}")
      return None
