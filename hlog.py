#!/usr/bin/python
# coding: utf-8
import logging
import logging.handlers
from logging import *
from datetime import *
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

rht = logging.handlers.TimedRotatingFileHandler("log/trading.log", 'D')
fmt = logging.Formatter("[%(levelname)s\t] %(asctime)s %(filename)s:%(lineno)s %(message)s", "%Y-%m-%d %H:%M:%S")
rht.setFormatter(fmt)
logger.addHandler(rht)

log_debug = logger.debug
critical = logger.critical
log_info = logger.info
log_warn = logger.warn
log_error = logger.error
