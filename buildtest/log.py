"""
Methods related to buildtest logging
"""
import logging
import os

from buildtest.defaults import BUILDTEST_LOGFILE, console
from buildtest.utils.file import create_dir
from rich.logging import RichHandler


def init_logfile(logfile=BUILDTEST_LOGFILE, debug=None, loglevel="DEBUG"):
    """Initialize a log file intended for a builder. This requires
    passing the filename intended for the log (from the builder)
    and returns the logger.

    Args:
        logfile (str): Path to logfile where buildtest will write logs
        debug (bool, optional): To enable debugging of logs to stdout. This option is enabled via ``buildtest --debug``
        loglevel (str, optional): This option will configure the loglevel by running `logging.setLevel <https://docs.python.org/3/library/logging.html#logging.Logger.setLevel>`_. This option is passed via ``buildtest --loglevel``
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
    logger.setLevel(loglevel)

    # enable StreamHandler when --debug option is enabled
    if debug:
        rich_handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_level=True,
            level=logging.NOTSET,
        )

        logger.addHandler(rich_handler)

    return logger
