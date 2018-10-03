
# importing module
import logging
import logging.handlers
import sys


def getLogger(logger_name, test=None):
    """ The method generates a logger instance to be reused.

    :param logger_name: incoming logger name
    :return: logger instance
    """

    logger = logging.getLogger(str(logger_name))
    log_level = logging.DEBUG
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')

    filepath = 'log/service.log'
    if test:
        filepath = 'log/test.log'

    fh = logging.handlers.RotatingFileHandler(filepath, maxBytes=104857600, backupCount=5)
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(log_level)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger

