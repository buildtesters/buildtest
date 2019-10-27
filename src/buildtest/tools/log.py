"""
Methods related to buildtest logging
"""
import os
import logging
from datetime import datetime
from buildtest.tools.config import logID, config_opts

class BuildTestError(Exception):
    """Class responsible for error handling in buildtest. This is a sub-class
    of Exception class."""
    def __init__(self, msg, *args):
        """Constructor Method.

        :param msg: message to print
        :type msg: str, required
        :param args:
        :type args:
        """
        if args:
            msg = msg % args
        self.msg = msg

    def __str__(self):
        return(repr(self.msg))

def init_log():
    """Initialize log file and define log attributes. This method invokes
    datetime.now() to name logfile using strftime().

    :return: Returns logger object and log path and logfile name
    :rtype: multiple return types (logger object, logpath, logfile)
    """
    fname = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.log")
    BUILDTEST_LOGDIR = os.path.join(config_opts['BUILDTEST_TESTDIR'],"log")

    logfile = os.path.join(BUILDTEST_LOGDIR, fname)
    # if log directory is not present create it automatically
    if not os.path.exists(BUILDTEST_LOGDIR):
        os.makedirs(BUILDTEST_LOGDIR)

    logger = logging.getLogger(logID)
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] - [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

    return logger, logfile
