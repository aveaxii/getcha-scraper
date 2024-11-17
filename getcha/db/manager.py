import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from colorlog_config import logger
from db.models import Base  
from db.main import init_db
from dotenv import load_dotenv
load_dotenv()

# Определяем режим работы
mode = os.getenv('MODE', 'PROD')

def recreate_schema():
    """Drops and recreates the 'public' schema if the project is in DEV mode."""
    if mode == 'DEV':
        db_uri = os.getenv('LOCAL_DB_URI')
        
        engine = create_engine(db_uri)
        conn = engine.connect()
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        
        try:
            conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
            logger.warning("Schema 'public' dropped.")
        except ProgrammingError as e:
            logger.critical(f"Error dropping schema: {e}")
        
        try:
            conn.execute(text("CREATE SCHEMA public"))
            logger.warning("Schema 'public' created.")
        except ProgrammingError as e:
            logger.critical(f"Error creating schema: {e}")
        
        conn.close()
        return engine
    elif mode == 'PROD':
        logger.warning('Unavailable in production mode.')
    else:
        logger.critical('MODE must be either "DEV" or "PROD"')

def fill_db():
    """Creates database tables according to the models and fills them if necessary."""
    try:
        init_db()
        logger.warning("Database filled successfully.")
    except Exception as e:
        logger.critical(f"Error while executing init_db: {e}")

def recreate_db():
    """Drops the schema and recreates the entire database, including tables, if the project is in DEV mode."""
    if mode == 'DEV':
        engine = recreate_schema()
        if engine:
            Base.metadata.create_all(engine)
            fill_db()
    elif mode == 'PROD':
        logger.warning('Unavailable in production mode. Use "db fill" instead.')
    else:
        logger.critical('MODE must be either "DEV" or "PROD"')