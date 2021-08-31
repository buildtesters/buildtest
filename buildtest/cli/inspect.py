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
        inspect_list(
            report, terse=args.terse, header=args.no_header, builder=args.builder
        )
        return

    # implements command 'buildtest inspect name'
    if args.inspect == "name":
        inspect_by_name(report, args.name, args.all)
        return

    if args.inspect == "query":
        inspect_query(report, args)
        return

    # implements command 'buildtest inspect id'
    if args.inspect == "id":
        inspect_by_id(report, args)
        return

    if args.inspect == "buildspec":
        inspect_buildspec(report, input_buildspecs=args.buildspec, all_records=args.all)


def inspect_list(report, terse=None, header=None, builder=None):
    """Implements method ``buildtest inspect list``"""

    test_ids = report._testid_lookup()

    table = {"name": [], "id": [], "buildspec": []}

    # implement command 'buildtest inspect list --builder'
    if builder:
        builders = report.builder_names()
        for name in builders:
            print(name)
        return

    # print output in terse format
    if terse:
        # print column headers if --no-header is not specified
        if not header:
            print("|".join(table.keys()))

        for identifier in test_ids.keys():
            print(
                f"{identifier}|{test_ids[identifier]['name']}|{test_ids[identifier]['buildspec']}"
            )

        return

    for identifier in test_ids.keys():
        # for name, buildspec in test_ids[identifier]:
        table["id"].append(identifier)
        table["name"].append(test_ids[identifier]["name"])
        table["buildspec"].append(test_ids[identifier]["buildspec"])

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
            print("executor: ", test["executor"])
            print("description: ", test["description"])
            print("state: ", test["state"])
            print("returncode: ", test["returncode"])
            print("runtime: ", test["runtime"])
            print("starttime: ", test["starttime"])
            print("endtime: ", test["endtime"])

            # print content of output file when 'buildtest inspect query --output' is set
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
                print()

            # print content of error file when 'buildtest inspect query --error' is set
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

            # print content of testpath when 'buildtest inspect query --testpath' is set
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

            # print content of build script when 'buildtest inspect query --buildscript' is set
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


def inspect_buildspec(report, input_buildspecs, all_records):
    """This method implements command ``buildtest inspect buildspec``"""

    search_buildspecs = []
    for fname in input_buildspecs:
        abs_fname = resolve_path(fname)

        if not abs_fname:
            print(f"buildspec: {fname} is not valid file")
            continue

        search_buildspecs.append(abs_fname)

    if not search_buildspecs:
        sys.exit(
            f"There are no buildspecs in cache based on input buildspecs: {input_buildspecs}"
        )

    # get raw content of test
    raw_content = report.get()
    # returns a list of buildspecs from the report cache
    available_buildspecs = list(report.get_buildspecs())

    # filter out buildspecs not found in report
    search_buildspecs = [
        buildspec
        for buildspec in search_buildspecs
        if buildspec in available_buildspecs
    ]

    # we stop if there are no buildspecs
    if not search_buildspecs:
        msg = "Unable to find any buildspecs in cache, please specify one of the following buildspecs: \n"
        for buildspec in available_buildspecs:
            msg += buildspec + "\n"
        sys.exit(msg)

    # dict used to hold records from
    records = {}

    for buildspec in search_buildspecs:
        records[buildspec] = raw_content[buildspec]

    # dict holding latest record of each test
    latest_records = {}
    if not all_records:
        for buildspec in records.keys():
            latest_records[buildspec] = {}
            for test in records[buildspec].keys():
                # get last element of list
                latest_records[buildspec][test] = records[buildspec][test][-1]

    records = latest_records or records
    print(json.dumps(records, indent=2))


def inspect_by_name(report, names, all_records):
    """Implements command ``buildtest inspect name`` which will print all test records
    by given name in JSON format.
    """

    records = {}
    raw_content = report.get()
    for buildspec in raw_content.keys():
        for name in names:
            if raw_content[buildspec].get(name):
                # if --all specified we get all records
                if all_records:
                    records[name] = raw_content[buildspec][name]
                # otherwise get last record of each test
                else:
                    records[name] = raw_content[buildspec][name][-1]

    if not records:
        sys.exit(
            f"Unable to find any records based on input name {names}. \n"
            f"Please select one of the following test names: {report.get_names()} \n"
        )
    print(json.dumps(records, indent=2))


def inspect_by_id(report, args):
    """This method implements ``buildtest inspect id`` command"""
    discovered_ids = []

    # discover all tests based on all unique ids from report cache
    for identifier in report.get_testids():
        for input_id in args.id:
            if identifier.startswith(input_id):
                discovered_ids.append(identifier)

    print("Discovered Test IDs: ", discovered_ids)
    # if no test discovered exit with message
    if not discovered_ids:
        sys.exit(
            f"Unable to find any test records based on id: {args.id}. We have found the following test ids: {report.get_testids()}"
        )

    records = report.fetch_records_by_ids(discovered_ids)
    print(json.dumps(records, indent=2))
