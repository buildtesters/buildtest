"""
Methods related to buildtest logging
"""
import logging
import os

from buildtest.defaults import BUILDTEST_LOGFILE
from buildtest.utils.file import create_dir


def init_logfile(logfile=BUILDTEST_LOGFILE, debug=None):
    """Initialize a log file intended for a builder. This requires
    passing the filename intended for the log (from the builder)
    and returns the logger.
    :param logfile: logfile name
    :type logfile: str
    """

    LOG_FORMATTER = "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] - [%(levelname)s] %(message)s"

    logger = logging.getLogger("buildtest")

    parent_dir = os.path.dirname(logfile)
    create_dir(parent_dir)

    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter(LOG_FORMATTER)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

    # enable StreamHandler when --debug option is enabled
    if debug:
        stdout_logger = logging.StreamHandler()
        stdout_logger.setLevel(logging.DEBUG)
        stdout_logger.setFormatter(formatter)

        logger.addHandler(stdout_logger)

    return logger
