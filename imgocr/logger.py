'''
日志模块
'''
import time
import logging
import logging.handlers
from log4mongo.handlers import MongoHandler
from configs.configs import *

LOG_FILENAME = 'main.log'
logger = logging.getLogger()


def set_logger(mongodb=False):
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
                                  '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if mongodb:
        # log output to mongodb
        db_name = 'logdbname'
        mon_handler = MongoHandler(host=mongodb_config['host'],
                                   port=int(mongodb_config['port']),
                                   database_name=db_name,
                                   username=mongodb_config['user'],
                                   password=mongodb_config['password'],
                                   authentication_db=db_name)
        mon_handler.setLevel(logging.INFO)
        logger.addHandler(mon_handler)
    else:
        # log output to file
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
        logger.addHandler(file_handler)


set_logger()
