"""This module implements methods for buildtest inspect command that can be used
to retrieve test record from report file in JSON format."""

import sys

from buildtest.cli.report import Report
from buildtest.defaults import BUILD_REPORT, console
from buildtest.utils.file import read_file, resolve_path
from rich.pretty import pprint
from rich.syntax import Syntax
from rich.table import Column, Table


def inspect_cmd(args):
    """Entry point for ``buildtest inspect`` command

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
    """

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
        inspect_by_name(report, args.name)
        return

    if args.inspect == "query":
        inspect_query(report, args)
        return

    if args.inspect == "buildspec":
        inspect_buildspec(report, input_buildspecs=args.buildspec, all_records=args.all)


def inspect_list(report, terse=None, header=None, builder=None):
    """This method list an output of test id, name, and buildspec file from the report cache. The default
    behavior is to display output in table format though this can be changed with terse format which will
    display in parseable format. This method implements command ``buildtest inspect list``

    Args:
        report (str): Path to report file
        terse (bool, optional): Print output in terse format
        header (bool, optional): Determine whether to print header in terse format.
        builder (bool, optional): Print output in builder format which can be done via ``buildtest inspect list --builder``

    """

    test_ids = report._testid_lookup()

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
            print("name|id|buildspec")

        for identifier in test_ids.keys():
            print(
                f"{identifier}|{test_ids[identifier]['name']}|{test_ids[identifier]['buildspec']}"
            )

        return

    table = Table(
        "[blue]name",
        "[blue]id",
        Column(header="[blue]buildspec", overflow="fold"),
        title="Test Summary by name, id, buildspec",
    )
    for identifier in test_ids.keys():
        table.add_row(
            identifier, test_ids[identifier]["name"], test_ids[identifier]["buildspec"]
        )
    console.print(table)


def inspect_query(report, args):
    """Entry point for ``buildtest inspect query`` command.

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
        report (str): Path to report file
    """

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
            console.rule(name + "/" + test["full_id"])

            console.print("executor: ", test["executor"])
            console.print("description: ", test["description"])
            console.print("state: ", test["state"])
            console.print("returncode: ", test["returncode"])
            console.print("runtime: ", test["runtime"])
            console.print("starttime: ", test["starttime"])
            console.print("endtime: ", test["endtime"])

            # print content of output file when 'buildtest inspect query --output' is set
            if args.output:

                content = read_file(test["outfile"])
                console.rule(f"Output File: {test['outfile']}")

                syntax = Syntax(content, "text")
                console.print(syntax)

            # print content of error file when 'buildtest inspect query --error' is set
            if args.error:
                content = read_file(test["errfile"])
                console.rule(f"Error File: {test['errfile']}")

                syntax = Syntax(content, "text")
                console.print(syntax)

            # print content of testpath when 'buildtest inspect query --testpath' is set
            if args.testpath:
                content = read_file(test["testpath"])
                console.rule(f"Test File: {test['testpath']}")

                syntax = Syntax(content, "shell", line_numbers=True, theme="emacs")
                console.print(syntax)

            # print content of build script when 'buildtest inspect query --buildscript' is set
            if args.buildscript:
                content = read_file(test["build_script"])
                console.rule(f"Test File: {test['build_script']}")

                syntax = Syntax(content, "shell", line_numbers=True, theme="emacs")
                console.print(syntax)


def inspect_buildspec(report, input_buildspecs, all_records):
    """This method implements command ``buildtest inspect buildspec``

    Args:
        report (str): Path to report file
        input_buildspecs (list): List of buildspecs to search in report file. This is specified as positional arguments to ``buildtest inspect buildspec``
        all_records (bool): Determine whether to display all records for every test that matches the buildspec. By default we retrieve the latest record.
    """

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

    pprint(records)


def inspect_by_name(report, names):
    """Implements command ``buildtest inspect name`` which will print all test records by given name in JSON format.

    .. code-block:: console

        # get last run for test exit1_fail
        buildtest inspect name exit1_fail

    .. code-block:: console

        # get record exit1_fail that starts with id 123
        buildtest inspect name exit1_fail/123

    Args:
        report (str): Path to report file
        names (list): List of test names to search in report file. This is specified as positional arguments to ``buildtest inspect name``
    """

    records = {}

    name_lookup = report.lookup()
    query_builders = []

    for name in names:
        # if test includes backslash we need to check if their is an ID match
        if name.find("/") != -1:
            test_name = name.split("/")[0]
            tid = name.split("/")[1]

            if test_name not in name_lookup.keys():
                console.print(f"Unable to find test: {test_name} so skipping test")
                continue

            # for list of all TEST IDs corresponding to test, get first test ID that startswith same character as input ID
            for full_ids in name_lookup[test_name]:
                if full_ids.startswith(tid):
                    query_builders.append(f"{test_name}/{full_ids}")
                    break

        # get latest test id for given test name
        else:
            tid = report.latest_testid_by_name(name)
            if tid:
                query_builders.append(f"{name}/{tid}")

    if not query_builders:
        sys.exit("Unable to find any tests, please try again")

    query_builders = list(set(query_builders))
    console.print(
        f"We have detected {len(query_builders)} builders with the following names {query_builders}"
    )

    for builder in query_builders:
        tid = builder.split("/")[1]
        name = builder.split("/")[0]
        if not records.get(name):
            records[name] = []

        records[name].append(report.fetch_records_by_ids([tid]))

    pprint(records)
