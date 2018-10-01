
# importing module
import logging
import logging.handlers
import sys


def getLogger(logger):
    logger = logging.getLogger(str(logger))
    log_level = logging.DEBUG
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')

    fh = logging.handlers.RotatingFileHandler('log/service.log', maxBytes=104857600, backupCount=5)
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(log_level)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger
