"""
Methods related to buildtest logging
"""
import os
import logging
from datetime import datetime
from buildtest.defaults import logID


def init_log(config_opts):
    """Initialize log file and define log attributes. This method invokes
       datetime.now() to name logfile using strftime().

    :return: Returns logger object and log path and logfile name
    :rtype: multiple return types (logger object, logpath, logfile)
    """
    fname = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.log")
    BUILDTEST_LOGDIR = os.path.join(config_opts["build"]["testdir"], "log")

    logfile = os.path.join(BUILDTEST_LOGDIR, fname)
    # if log directory is not present create it automatically
    if not os.path.exists(BUILDTEST_LOGDIR):
        os.makedirs(BUILDTEST_LOGDIR)

    logger = logging.getLogger(logID)
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] - [%(levelname)s] %(message)s"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

    return logger, logfile
