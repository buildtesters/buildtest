import logging
import tempfile
from buildtest.log import BuildTestLogger, LOG_FORMATTER
from buildtest.utils.file import read_file


def test_BuildTestLogger():

    logger = BuildTestLogger("buildtest")
    # at startup, we don't have any handlers set
    assert not logger.hasHandlers()
    # ensure we have effective level of 10 (DEBUG)
    assert logger.getEffectiveLevel() == 10

    tf = tempfile.NamedTemporaryFile()

    logger.add_filehandler(tf.name, LOG_FORMATTER)
    logger.add_streamhandler(LOG_FORMATTER, logging.ERROR)
    assert logger.name == "buildtest"

    # writing message at each log level
    logger.debug("DEBUG MESSAGE")
    logger.info("INFO MESSAGE")
    logger.warning("WARNING MESSAGE!")
    logger.error("ERROR MESSAGE!!")
    logger.critical("CRITICAL MESSAGE!!!")
    content = read_file(tf.name)
    print(content)
