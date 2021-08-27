import os

from buildtest.cli.report import Report
from buildtest.exceptions import BuildTestError


def change_directory(test):
    """Given a test name we will change directory to root of test for last test run. This
    method implements command ``buildtest cd``

    :param test: name of test found in test report
    :type test: str
    """

    report = Report()
    names = report.get_names()
    if test not in names:
        raise BuildTestError(f"Please specify one of the following test names: {names}")

    testroot = report.get_testroot_by_name(test)
    os.chdir(testroot)
    print(f"Changing directory to root of test: {test}")
    shell = os.environ.get("SHELL", "/bin/sh")
    os.execl(shell, shell)
