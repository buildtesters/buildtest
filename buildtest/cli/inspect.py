"""This module implements methods for buildtest inspect command that can be used
to retrieve test record from report file in JSON format."""

import json
import os
import sys
from termcolor import colored
from tabulate import tabulate

from buildtest.defaults import BUILD_REPORT
from buildtest.utils.file import load_json, resolve_path


def inspect_cmd(args):
    """Entry point for ``buildtest inspect`` command"""

    report_file = resolve_path(args.report_file) or BUILD_REPORT

    report = load_json(report_file)

    assert isinstance(report, dict)
    test_ids = get_all_ids(report)

    print(f"Reading Report File: {report_file} \n")

    # implements command 'buildtest inspect list'
    if args.inspect == "list":
        inspect_list(test_ids)
        return

    # implements command 'buildtest inspect name'
    if args.inspect == "name":
        inspect_by_name(report, args.name)
        return

    # implements command 'buildtest inspect id'
    if args.inspect == "id":
        inspect_by_id(test_ids, report, args)


def get_all_ids(report):
    """Return all unique test ids from report cache

    :param report: loaded report file in JSON format
    :type report: dict
    :return: a dictionary returning a list of unique test IDs
    :rtype: dict
    """

    test_id = {}

    for buildspec in report.keys():
        # loop over all tests in buildspecs
        for name in report[buildspec].keys():
            # loop over each test entry for given test
            for test in report[buildspec][name]:
                # test_id.append(test["full_id"])
                test_id[test["full_id"]] = name

    return test_id


def inspect_list(test_ids):
    """Implements method ``buildtest inspect list``"""

    table = {"name": [], "id": []}
    for identifier, name in test_ids.items():
        table["name"].append(name)
        table["id"].append(identifier)

    if os.getenv("BUILDTEST_COLOR") == "True":
        print(
            tabulate(
                table,
                headers=[
                    colored(field, "blue", attrs=["bold"]) for field in table.keys()
                ],
                tablefmt="grid",
            )
        )
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
            f"Unable to find any records based on {names}. Please run 'buildtest inspect list' and see list of test names."
        )

    print(json.dumps(records, indent=2))


def inspect_by_id(test_ids, report, args):
    discovered_ids = []
    records = {}

    # discover all tests based on all unique ids from report cache
    for identifier in test_ids.keys():
        for input_id in args.id:
            if identifier.startswith(input_id):
                discovered_ids.append(identifier)

    # if no test discovered exit with message
    if not discovered_ids:
        sys.exit(
            f"Unable to find any test records based on id: {args.id}, please run 'buildtest inspect list' to see list of ids."
        )

    for buildspec in report.keys():
        for test in report[buildspec].keys():
            for test_record in report[buildspec][test]:
                for identifier in discovered_ids:
                    if test_record["full_id"] == identifier:
                        records[identifier] = test_record

    print(json.dumps(records, indent=2))
