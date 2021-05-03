"""
Methods related to buildtest logging
"""
import logging
import os
import sys


LOG_FORMATTER = "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] - [%(levelname)s] %(message)s"
LOG_NAME = "buildtest"
FILE_LOG = os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log")


def init_logfile(logfile=FILE_LOG):
    """Initialize a log file intended for a builder. This requires
    passing the filename intended for the log (from the builder)
    and returns the logger.
    :param logfile: logfile name
    :type logfile: str
    """

    logger = logging.getLogger("buildtest")
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter(LOG_FORMATTER)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

    return logger
