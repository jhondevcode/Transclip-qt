import datetime
import logging
import os

from transclip.homedir import get_home_path

LOG_DIR = os.path.join(get_home_path(), "logs")

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

log_file_name = f"log-{datetime.datetime.now().date()}.log"
log_file = os.path.join(LOG_DIR, log_file_name)
logging.basicConfig(filename=log_file, format="%(asctime)s %(message)s", filemode="a")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def info(msg, *args, **kwargs):
    logger.info(msg, args, kwargs)


def warning(msg, *args, **kwargs):
    logger.warning(msg, args, kwargs)


def error(msg, *args, **kwargs):
    logger.error(msg, args, kwargs)
