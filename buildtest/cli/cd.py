import os
import sys

from buildtest.cli.report import Report


def change_directory(test):
    """Given a test name we will change directory to root of test for last test run. This
    method implements command ``buildtest cd``

    Args:
        test (str): Name of test found in test report. The test is specified via ``buildtest cd <test>``
    """

    report = Report()

    builders = report.builder_names()

    tid = None
    name = None
    # if input name contains a '/' followed by TEST ID we will match id
    if test.find("/") != -1:
        name = test.split("/")[0]

        for builder in builders:
            if builder.startswith(test):
                tid = builder.split("/")[1]
                break

    else:
        name = test
        tid = report.latest_testid_by_name(test)

    if not tid:
        print("Please select one of the following builders:")
        for builder in builders:
            print(builder)
        sys.exit(1)

    record = report.fetch_records_by_ids([tid])

    testroot = record[tid]["testroot"]

    os.chdir(testroot)
    print(f"Changing directory to root of test: {name}/{tid}")

    shell = os.environ.get("SHELL", "/bin/bash")
    os.execl(shell, shell)
