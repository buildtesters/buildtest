"""This module implements methods for buildtest inspect command that can be used
to retrieve test record from report file in JSON format."""

import json
import os
import sys

from buildtest.cli.report import Report
from buildtest.defaults import BUILD_REPORT
from buildtest.utils.file import read_file, resolve_path
from tabulate import tabulate
from termcolor import colored


def inspect_cmd(args):
    """Entry point for ``buildtest inspect`` command"""

    report_file = BUILD_REPORT
    if args.report:

        report_file = resolve_path(args.report)

    report = Report(report_file)

    # if not args.parse:
    #    print(f"Reading Report File: {report_file} \n")

    # implements command 'buildtest inspect list'
    if args.inspect == "list":
        inspect_list(report, terse=args.terse)
        return

    # implements command 'buildtest inspect name'
    if args.inspect == "name":
        inspect_by_name(report, args.name)
        return

    if args.inspect == "query":
        inspect_query(report, args)
        return

    # implements command 'buildtest inspect id'
    if args.inspect == "id":
        inspect_by_id(report, args)


def inspect_list(report, terse=None):
    """Implements method ``buildtest inspect list``"""

    test_ids = report.get_ids()

    table = {"name": [], "id": []}
    if terse:
        for uid, name in test_ids.items():
            print(f"{uid}|{name}")
        return
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


def inspect_query(report, args):
    """Entry point for ``buildtest inspect query`` command."""

    records = {}

    raw_content = report.get()
    for buildspec in raw_content.keys():
        for name in args.name:
            if raw_content[buildspec].get(name):
                records[name] = raw_content[buildspec][name]

    # if no records based on input name, we raise an error
    if not records:
        sys.exit(
            f"Unable to find any records based on {args.name}. According to report file: {report.reportfile()} we found the following test names: {report.get_names()}."
        )
    for name, test_record in records.items():

        # the default is to print the last record (latest record)
        tests = [test_record[-1]]

        # print the first record if --display first is set
        if args.display == "first":
            tests = [test_record[0]]
        elif args.display == "all":
            tests = test_record

        for test in tests:
            print(
                "{:_<30}".format(""),
                name,
                f"(ID: {test['full_id']})",
                "{:_<30}".format(""),
            )
            print("description: ", test["description"])
            print("state: ", test["state"])
            print("returncode: ", test["returncode"])
            print("runtime: ", test["runtime"])
            print("starttime: ", test["starttime"])
            print("endtime: ", test["endtime"])

            # print content of output file when 'buildtest inspect display --output' is set
            if args.output:

                content = read_file(test["outfile"])
                print(
                    "{:*<25}".format(""),
                    f"Start of Output File: {test['outfile']}",
                    "{:*<25}".format(""),
                )
                print(content)
                print(
                    "{:*<25}".format(""),
                    f"End of Output File: {test['outfile']}",
                    "{:*<25}".format(""),
                )
                # print("{:^<40}".format(''), "End of Output File","{:^<40}".format(''))
                print()

            # print content of error file when 'buildtest inspect display --error' is set
            if args.error:
                content = read_file(test["errfile"])
                print(
                    "{:*<25}".format(""),
                    "Start of Error File: ",
                    test["errfile"],
                    "{:*<25}".format(""),
                )
                print(content)
                print(
                    "{:*<25}".format(""),
                    "End of Error File: ",
                    test["errfile"],
                    "{:*<25}".format(""),
                )

                print()

            # print content of testpath when 'buildtest inspect display --testpath' is set
            if args.testpath:
                content = read_file(test["testpath"])
                print(
                    "{:*<25}".format(""),
                    "Start of Test Path: ",
                    test["testpath"],
                    "{:*<25}".format(""),
                )
                print(content)
                print(
                    "{:*<25}".format(""),
                    "End of Test Path: ",
                    test["testpath"],
                    "{:*<25}".format(""),
                )
                print()

            # print content of build script when 'buildtest inspect display --buildscript' is set
            if args.buildscript:
                content = read_file(test["build_script"])
                print(
                    "{:*<25}".format(""),
                    "Start of Build Script: ",
                    test["build_script"],
                    "{:*<25}".format(""),
                )
                print(content)
                print(
                    "{:*<25}".format(""),
                    "End of Build Script: ",
                    test["build_script"],
                    "{:*<25}".format(""),
                )
                print()


def inspect_by_name(report, names):
    """Implements command ``buildtest inspect name`` which will print all test records
    by given name in JSON format.
    """

    records = {}
    raw_content = report.get()
    for buildspec in raw_content.keys():
        for name in names:
            if raw_content[buildspec].get(name):
                records[name] = raw_content[buildspec][name]

    if not records:
        sys.exit(
            f"Unable to find any records based on input name {names}. \n"
            f"Please select one of the following test names: {report.get_names()} \n"
        )
    print(json.dumps(records, indent=2))


def inspect_by_id(report, args):
    discovered_ids = []
    records = {}

    # discover all tests based on all unique ids from report cache
    for identifier in report.get_ids():
        for input_id in args.id:
            if identifier.startswith(input_id):
                discovered_ids.append(identifier)

    # if no test discovered exit with message
    if not discovered_ids:
        sys.exit(
            f"Unable to find any test records based on id: {args.id}, please run 'buildtest inspect list' to see list of ids."
        )

    report_content = report.get()

    for buildspec in report_content.keys():
        for test in report_content[buildspec].keys():
            for test_record in report_content[buildspec][test]:
                for identifier in discovered_ids:
                    if test_record["full_id"] == identifier:
                        records[identifier] = test_record

    print(json.dumps(records, indent=2))
