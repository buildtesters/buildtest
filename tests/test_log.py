import os
from buildtest.log import init_logfile
from buildtest.utils.file import read_file


def test_init_logfile(tmp_path):
    logfile = os.path.join(tmp_path, "buildtest.log")
    print(f"Logfile: {logfile}")

    logger = init_logfile(logfile)
    assert logger

    # check if handler is defined
    assert logger.hasHandlers()
    # check if Log Level is set to DEBUG (10)
    assert logger.getEffectiveLevel() == 10

    # writing message at each log level
    logger.debug("DEBUG MESSAGE")
    logger.info("INFO MESSAGE")
    logger.warning("WARNING MESSAGE!")
    logger.error("ERROR MESSAGE!!")
    logger.critical("CRITICAL MESSAGE!!!")
    content = read_file(logfile)
    print(content)
