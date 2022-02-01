"""
Methods related to buildtest logging
"""
import logging
import os

from buildtest.defaults import BUILDTEST_LOGFILE, console
from buildtest.utils.file import create_dir
from rich.logging import RichHandler


def init_logfile(logfile=BUILDTEST_LOGFILE, debug=None):
    """Initialize a log file intended for a builder. This requires
    passing the filename intended for the log (from the builder)
    and returns the logger.
    :param logfile: logfile name
    :type logfile: str
    """

    formatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] - [%(levelname)s] %(message)s"
    )

    logger = logging.getLogger("buildtest")

    parent_dir = os.path.dirname(logfile)
    create_dir(parent_dir)

    fh = logging.FileHandler(logfile)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

    # enable StreamHandler when --debug option is enabled
    if debug:
        rich_handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            markup=True,
            show_time=False,
            show_level=False,
            level=logging.NOTSET,
        )
        rich_handler.setFormatter(formatter)
        logger.addHandler(rich_handler)

    return logger
