from datetime import datetime
from sqlalchemy import (
    JSON, Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Enum, ARRAY, PrimaryKeyConstraint, func
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class AttributeType(enum.Enum):
    BRAND = 'BRAND'
    MODEL = 'MODEL'
    SUBMODEL = 'SUBMODEL'
    SERIES_NAME = 'SERIES_NAME'
    DETAILED_GRADE = 'DETAILED_GRADE'
    ATTRIBUTE = 'ATTRIBUTE'
    COUNTRY = 'COUNTRY'

class AvailableAttribute(Base):
    __tablename__ = 'available_attributes'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=True)
    att_type = Column(Enum(AttributeType), default=AttributeType.ATTRIBUTE, nullable=False)
    parent_att = Column(Integer, ForeignKey('available_attributes.id'), nullable=True)
    description = Column(Text, nullable=True)
    last_update = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    ordering = Column(Integer, nullable=True)

    parent = relationship('AvailableAttribute', remote_side=[id], backref='children')

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    phone = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    message = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

class ReviewImage(Base):
    __tablename__ = 'review_images'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

class Seller(Base):
    __tablename__ = 'seller'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False)
    username = Column(String(255), nullable=True)
    username_ru = Column(String(255), nullable=True)
    company_name = Column(String(500), nullable=True)
    company_name_ru = Column(String(500), nullable=True)
    association_name = Column(String(500), nullable=True)
    association_name_ru = Column(String(500), nullable=True)
    phone = Column(String(500), nullable=True)
    last_update = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

class TaskExecution(Base):
    __tablename__ = 'task_execution'

    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    spider_progress = Column(String(255), nullable=True)
    completed = Column(Integer, default=0, nullable=False)

class Page(Base):
    __tablename__ = 'page'

    id = Column(Integer, primary_key=True)
    type = Column(Integer, default=0, nullable=False)
    url = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey('task_execution.id', ondelete='SET NULL'), nullable=True)
    parsed = Column(Integer, default=0, nullable=False)
    last_update = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    task = relationship('TaskExecution', backref='pages')

class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True)
    car_id = Column(String(100), nullable=False) # WARNING: in original intercar this table is integer
    page_id = Column(Integer, ForeignKey('page.id', ondelete='SET NULL'), nullable=True)
    title = Column(String(500), nullable=False)
    title_ru = Column(String(500), nullable=True)
    price = Column(Integer, nullable=False)
    images = Column(ARRAY(Text), nullable=True)
    seller_id = Column(Integer, ForeignKey('seller.id', ondelete='SET NULL'), nullable=True)
    external_url = Column(Text, nullable=True)
    color = Column(String(500), nullable=True)
    color_ru = Column(String(500), nullable=True)
    distance = Column(Integer, nullable=False)
    production_year = Column(Integer, nullable=False)
    fuel_type = Column(String(500), nullable=False)
    fuel_type_ru = Column(String(500), nullable=True)
    v_type = Column(String(500), nullable=False)
    v_type_ru = Column(String(500), nullable=True)
    registration_date = Column(DateTime, nullable=True)
    last_update = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    sold = Column(Boolean, default=False, nullable=False)
    ready = Column(Boolean, default=False, nullable=False)

    page = relationship('Page', backref='cars')
    seller = relationship('Seller', backref='cars')

class CarAttribute(Base):
    __tablename__ = 'car_attributes'

    attribute_id = Column(Integer, ForeignKey('available_attributes.id', ondelete='CASCADE'), nullable=False)
    car_id = Column(Integer, ForeignKey('car.id', ondelete='CASCADE'), nullable=False)
    value = Column(String(255), nullable=False)
    value_ru = Column(String(255), nullable=True)

    __table_args__ = (PrimaryKeyConstraint('attribute_id', 'car_id', name='cat_attribute_pk'),)

    attribute = relationship('AvailableAttribute', backref='car_attributes')
    car = relationship('Car', backref='attributes')

class PageAttribute(Base):
    __tablename__ = 'page_attributes'

    attribute_id = Column(Integer, ForeignKey('available_attributes.id', ondelete='CASCADE'), nullable=False)
    page_id = Column(Integer, ForeignKey('page.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (PrimaryKeyConstraint('attribute_id', 'page_id', name='page_attribute_pk'),)

    attribute = relationship('AvailableAttribute', backref='page_attributes')
    page = relationship('Page', backref='attributes')

class Translation(Base):
    __tablename__ = 'translations'

    id = Column(Integer, primary_key=True)
    original = Column(String(255), nullable=False)
    ru = Column(String(255), nullable=True)

class Metadata(Base):
    __tablename__ = 'metadata'

    id = Column(Integer, primary_key=True)
    auction_date = Column(Integer, nullable=True)
    total_cars = Column(Integer, nullable=True)
    cookies = Column(JSON, nullable=True)  
    last_update = Column(DateTime, default=lambda: datetime.now())
