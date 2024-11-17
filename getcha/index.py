"""entrypoint for scraper"""

import os
import shutil
import sys
import subprocess

from colorlog_config import logger
from dotenv import load_dotenv, dotenv_values
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor
from db.main import get_session_local
from db.manager import fill_db, recreate_db

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
from twisted.internet import defer, reactor

load_dotenv()

mode = os.getenv('MODE', 'PROD')

settings = get_project_settings()

env_vars = dotenv_values("./../.env")
for env_name in env_vars:
    settings.set(env_name, env_vars[env_name])

LOG_FILE_NAME=settings.get("LOG_FILE")
if LOG_FILE_NAME:
    try:
    # Remove the file
        os.remove(LOG_FILE_NAME)
        print(f"{LOG_FILE_NAME} has been removed successfully.")
    except Exception:
        print(f"{LOG_FILE_NAME} not found. No action taken.")
    log_dir, log_file = os.path.split(LOG_FILE_NAME)
    if len(log_dir) > 0 and not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    print(f"Script started. See full log in: {LOG_FILE_NAME}")


settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
configure_logging(settings)
runner = CrawlerRunner(settings)

       
@defer.inlineCallbacks
def my_pw_crawl():
    """this one uses playwright"""
    check_mode()
    # yield runner.crawl(DamageInfoSpider)
    reactor.stop()

@defer.inlineCallbacks
def my_crawl():
    """main sequental runner"""
    logger.critical('main sequental runner')
    check_mode()
    # yield runner.crawl(LoginSpider)
    # yield runner.crawl(InitialInfoSpider)
    # yield runner.crawl(DetailInfoSpider)
    # yield runner.crawl(InsuranceInfoSpider)
    # yield runner.crawl(ImagesInfoSpider)
    reactor.stop()
    
    
# ----------------------------------------------------------------
    
# def run_index():
#     task_id = create_task_exec()
    
#     try:
#         logger.info(f'Task ID {task_id} started successfully.')
        
#         settings.set('TASK_ID', task_id)
        
#         if len(sys.argv) == 3:
#             my_pw_crawl()
#         else:
#             cleanup_old_car_pages()
#             cleanup_old_cars()
#             my_crawl()

#         reactor.run()
#     except Exception as e:
#         logger.error(f'Error during script execution: {e}')
#     finally:
#         mark_task_completed(task_id)
#         logger.info(f'Task ID {task_id} completed successfully.')
        
# def create_task_exec():
#     session = get_session_local()
#     task = LotteTaskExecution()
#     session.add(task)
#     session.commit()
#     task_id = task.id
#     session.close()
#     return task_id

# def mark_task_completed(task_id):
#     session = get_session_local()
#     task = session.get(LotteTaskExecution, task_id)
#     if task:
#         task.completed = 1
#         session.commit()
#     session.close()


def check_mode():
    logger.warning(f'Chosen mode is: {mode}')
    
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "db":
        if len(sys.argv) > 2:
            command = sys.argv[2]
            if command == "recreate" and mode == 'DEV':
                recreate_db()
            elif command == "fill":
                fill_db()
            elif command == "clean_pages":    
                cleanup_old_car_pages()
            elif command == "clean_cars":
                cleanup_old_cars()
            elif command == "test_images" and mode == 'DEV':
                # test_fetch_images_from_ins_info()
                # test_fetch_images_from_kcar_car()
                print("test_fetch_images_from_ins_info")
            elif command == "check_mode":
                check_mode()
                print("Available commands for DEV mode: recreate, fill, clean_pages, clean_cars, test_images.\nAvailable commands for PROD mode: fill, clean_pages, clean_cars")
            else:
                check_mode()
                print("Unknown database command.\nAvailable commands for DEV mode: recreate, fill, clean_pages, clean_cars, test_images.\nAvailable commands for PROD mode: fill, clean_pages, clean_cars")
    else:
        logger.critical('Crawler created')
        # run_index()