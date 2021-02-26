# -*- coding: utf-8 -*-
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

__LOGGING_MSG_FORMAT = '%(asctime)s|%(levelname)s|%(lineno)d|%(message)s||'
__LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
__formatter = logging.Formatter(__LOGGING_MSG_FORMAT, __LOGGING_DATE_FORMAT)

logging.basicConfig(level=logging.INFO, format=__LOGGING_MSG_FORMAT, datefmt=__LOGGING_DATE_FORMAT)

__handle = logging.handlers.TimedRotatingFileHandler('{}.log'.format(sys.argv[0]), 'midnight', 1, 6)
__handle.suffix = "%Y-%m-%d.log"
__handle.setFormatter(__formatter)
__handle.setLevel(logging.INFO)

#logger = logging.getLogger(__name__)
#logger.addHandler(__handle)

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.level = logging.DEBUG
logger.addHandler(stream_handler)