#!/usr/bin/python
# coding: utf-8
import logging
import logging.handlers
from logging import *
import datetime

"""
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

rht = logging.handlers.TimedRotatingFileHandler("log/trading.log", 'D')
fmt = logging.Formatter("[%(levelname)s\t] %(asctime)s %(filename)s:%(lineno)s %(message)s", "%Y-%m-%d %H:%M:%S")
rht.setFormatter(fmt)
logger.addHandler(rht)

log_debug = logger.debug
critical = logger.critical
log_info = logger.info
log_warn = logger.warning
log_error = logger.error
"""

logger = logging.getLogger()
log_debug = logger.debug
critical = logger.critical
log_info = logger.info
log_warn = logger.warning
log_error = logger.error


def init(filepath, level=logging.DEBUG):
    logger.setLevel(level)
    rht = logging.handlers.TimedRotatingFileHandler(filepath, 'D')
    fmt = logging.Formatter("[%(levelname)s\t] %(asctime)s %(filename)s:%(lineno)s %(message)s", "%Y-%m-%d %H:%M:%S")
    rht.setFormatter(fmt)
    logger.addHandler(rht)
