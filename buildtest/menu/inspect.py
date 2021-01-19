import json
import os
import sys
from buildtest.defaults import BUILD_REPORT
from buildtest.utils.command import read_file


def get_all_ids():
    """Return all unique test ids from report cache
       :return: list of unique ids
       :rtype: list
    """

    test_id = []
    with open(BUILD_REPORT, "r") as fd:
        report = json.loads(fd.read())

    for buildspec in report.keys():
        # loop over all tests in buildspecs
        for name in report[buildspec].keys():
            # loop over each test entry for given test
            for test in report[buildspec][name]:
                test_id.append(test["full_id"])

    return test_id


def func_inspect(args):
    """Entry point for ``buildtest inspect`` command"""

    test_ids = get_all_ids()

    discovered_tests = []
    # discover all tests based on all unique ids from report cache
    for identifier in test_ids:
        if identifier.startswith(args.test):
            discovered_tests.append(identifier)

    # if no test discovered exit with message
    if not discovered_tests:
        sys.exit("Unable to find any test records")

    # exit if we find more than one unique test
    if len(discovered_tests) > 1:
        print(
            f"Detected {len(discovered_tests)} test records, please specify a unique test id"
        )

        for test in discovered_tests:
            print(test)
        sys.exit(0)

    with open(BUILD_REPORT, "r") as fd:
        report = json.loads(fd.read())

    record = {}
    input_buildspec = None
    # loop over all buildspecs
    for buildspec in report.keys():
        # loop over all tests in buildspecs
        for name in report[buildspec].keys():
            # loop over each test entry for given test
            for test in report[buildspec][name]:
                if test["full_id"].startswith(args.test):
                    for k, v in test.items():
                        record[k] = v
                        input_buildspec = buildspec

    print(json.dumps(record, indent=2))

    if os.path.exists(record["outfile"]):
        content = read_file(record["outfile"])

        print("\n\n")
        print("Output File")
        print("{:_<30}".format(""))
        print(content)

    if os.path.exists(record["errfile"]):
        content = read_file(record["errfile"])

        print("\n\n")
        print("Error File")
        print("{:_<30}".format(""))
        print(content)

    if os.path.exists(record["testpath"]):
        content = read_file(record["testpath"])

        print("\n\n")
        print("Test Content")
        print("{:_<30}".format(""))
        print(content)

    if input_buildspec:
        print("\n\n")
        print("buildspec: ", input_buildspec)
        print("{:_<30}".format(""))
        content = read_file(input_buildspec)
        print(content)
