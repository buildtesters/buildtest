import json
import os
import sys
from termcolor import colored
from tabulate import tabulate

from buildtest.defaults import BUILD_REPORT
from buildtest.utils.command import read_file
from buildtest.exceptions import BuildTestError

def get_all_ids():
    """Return all unique test ids from report cache
    :return: list of unique ids
    :rtype: list
    """

    test_id = {}
    if not os.path.exists(BUILD_REPORT):
        raise BuildTestError(f"Cannot find file {BUILD_REPORT}, please build a test via 'buildtest build' in order to generate report file.")

    with open(BUILD_REPORT, "r") as fd:
        report = json.loads(fd.read())

    for buildspec in report.keys():
        # loop over all tests in buildspecs
        for name in report[buildspec].keys():
            # loop over each test entry for given test
            for test in report[buildspec][name]:
                #test_id.append(test["full_id"])
                test_id[test['full_id']] = name

    return test_id


def func_inspect(args):
    """Entry point for ``buildtest inspect`` command"""


    # implements command 'buildtest inspect list'
    if args.subcommands == "list":
        inspect_list()
        return

    test_ids = get_all_ids()
    with open(BUILD_REPORT, "r") as fd:
        report = json.loads(fd.read())

    # implements command 'buildtest inspect name'
    if args.subcommands == "name":
        inspect_by_name(report, args.name)
        return

    # implements command 'buildtest inspect id'
    if args.subcommands == "id":

        discovered_ids = []
        records = {}

        # discover all tests based on all unique ids from report cache
        for identifier in test_ids.keys():
            for input_id in args.id:
                if identifier.startswith(input_id):
                    discovered_ids.append(identifier)

        # if no test discovered exit with message
        if not discovered_ids:
            sys.exit(f"Unable to find any test records based on id: {args.id}, please run 'buildtest inspect list' to see list of ids.")

        for buildspec in report.keys():
            for test in report[buildspec].keys():
                for test_record in report[buildspec][test]:
                    for identifier in discovered_ids:
                        if test_record["full_id"] == identifier:
                            records[identifier] = test_record

        print(json.dumps(records, indent=2))

def inspect_list():
    """Implements method ``buildtest inspect list``"""

    test_ids = get_all_ids()

    table = {"name": [], "id": []}
    for id, name in test_ids.items():
        table["name"].append(name)
        table["id"].append(id)

    if os.getenv("BUILDTEST_COLOR") == "True":
        print(tabulate(table, headers=[colored(field, 'blue', attrs=['bold']) for field in table.keys()], tablefmt="grid"))
        return
    print(tabulate(table, headers=table.keys(), tablefmt="grid"))

def inspect_by_name(report, names):
    """Implements command ``buildtest inspect name`` which will print all test records
       by given name in JSON format.
    """

    records = {}

    for buildspec in report.keys():
        for name in names:
            if report[buildspec].get(name):
                records[name] = report[buildspec][name]

    if not records:
        sys.exit(
            f"Unable to find any records based on {names}. Please run 'buildtest inspect list' and see list of test names.")

    print(json.dumps(records, indent=2))