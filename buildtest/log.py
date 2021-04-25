"""
Methods related to buildtest logging
"""
import logging
import os
import sys


LOG_FORMATTER = "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] - [%(levelname)s] %(message)s"
LOG_NAME = "buildtest"
FILE_LOG = os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log")


class BuildTestLogger(logging.Logger):
    def __init__(self, name="buildtest", level=10):
        super().__init__(name, level)
        self.logger = logging.getLogger(name)

    def add_filehandler(self, name, fmt):
        self.file_hander = logging.FileHandler(name)
        formatter = logging.Formatter(fmt)
        self.file_hander.setFormatter(formatter)
        self.file_hander.setLevel(logging.DEBUG)
        self.logger.addHandler(self.file_hander)

    def add_streamhandler(self, fmt=LOG_FORMATTER, level=logging.ERROR):
        self.stream_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(fmt)
        self.stream_handler.setFormatter(formatter)
        self.stream_handler.setLevel(level)
        self.logger.addHandler(self.stream_handler)


# a = BuildTestLogger("buildtest",0)

buildtest_logger = BuildTestLogger(LOG_NAME, logging.DEBUG)
buildtest_logger.add_filehandler(FILE_LOG, LOG_FORMATTER)
