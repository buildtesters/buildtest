"""
Methods related to buildtest logging
"""
import logging
from buildtest.defaults import logID


def init_logfile(logfile):
    """Initialize a log file intended for a builder. This requires
    passing the filename intended for the log (from the builder)
    and returns the logger.
    """
    logger = logging.getLogger(logID)
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] - [%(levelname)s] %(message)s"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

    return logger
