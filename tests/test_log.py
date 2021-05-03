import tempfile
from buildtest.log import init_logfile
from buildtest.utils.file import read_file


def test_BuildTestLogger():

    logger = init_logfile()

    # ensure we have effective level of 10 (DEBUG)
    assert logger.getEffectiveLevel() == 10

    tf = tempfile.NamedTemporaryFile()

    assert logger.name == "buildtest"

    # writing message at each log level
    logger.debug("DEBUG MESSAGE")
    logger.info("INFO MESSAGE")
    logger.warning("WARNING MESSAGE!")
    logger.error("ERROR MESSAGE!!")
    logger.critical("CRITICAL MESSAGE!!!")
    content = read_file(tf.name)
    print(content)
