from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from db.models import Base
import os
load_dotenv()

mode = os.getenv('MODE', 'PROD')
db_uri = os.getenv('DB_URI') if mode == 'PROD' else os.getenv('LOCAL_DB_URI')

engine = create_engine(db_uri)
session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))

def init_db():
  from db.models import AvailableAttribute, Question, ReviewImage, Seller, TaskExecution, Page, Car, CarAttribute, PageAttribute, Translation, Metadata
  Base.metadata.create_all(engine)
        
def get_session_local():
    return session()