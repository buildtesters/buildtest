"""This module implements methods for buildtest inspect command that can be used
to retrieve test record from report file in JSON format."""
import re
import sys

from buildtest.cli.report import Report
from buildtest.defaults import console
from buildtest.utils.file import read_file, resolve_path
from rich.pretty import pprint
from rich.syntax import Syntax
from rich.table import Column, Table


def inspect_cmd(args, report_file=None):
    """Entry point for ``buildtest inspect`` command

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
    """

    report = Report(report_file)

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


def fetch_test_names(report, names):
    """Return a list of builders given input test names by search the report file for valid records. If test is found it will be returned as a builder name. If names
    are specified without test ID then we retrieve latest record for test name. If names are specified with ID we find the first matching test record.
    """
    query_builders = []
    name_lookup = report.lookup()

    for name in names:
        # if test includes backslash we need to check if their is an ID match
        if name.find("/") != -1:
            test_name, tid = name.split("/")[0], "".join(name.split("/")[1:])

            if test_name not in name_lookup.keys():
                console.print(f"Unable to find test: {test_name} so skipping test")
                continue

            # for list of all TEST IDs corresponding to test name, apply a re.match to acquire builder names
            for full_ids in name_lookup[test_name]:
                # if full_ids.startswith(tid):
                if re.match(tid, full_ids):
                    query_builders.append(f"{test_name}/{full_ids}")

        # get latest test id for given test name
        else:
            tid = report.latest_testid_by_name(name)
            if tid:
                query_builders.append(f"{name}/{tid}")

    query_builders = list(set(query_builders))

    if not query_builders:
        console.print(
            f"Unable to find any tests by name {names}, please select one of the following tests: {report.get_names()}"
        )
        sys.exit(1)

    return query_builders


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
            console.print("[blue]id|name|buildspec")

        for identifier in test_ids.keys():
            console.print(
                f"{identifier}|{test_ids[identifier]['name']}|{test_ids[identifier]['buildspec']}"
            )

        return

    table = Table(
        "[blue]id",
        "[blue]name",
        Column(header="[blue]buildspec", overflow="fold"),
        title="Test Summary by name, id, buildspec",
    )
    for identifier in test_ids.keys():
        table.add_row(
            f"[red]{identifier}",
            f"[cyan]{test_ids[identifier]['name']}",
            f"[green]{test_ids[identifier]['buildspec']}",
        )
    console.print(table)


def inspect_query(report, args):
    """Entry point for ``buildtest inspect query`` command.

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
        report (str): Path to report file
    """

    records = {}
    query_builders = fetch_test_names(report, args.name)

    for builder in query_builders:
        tid = builder.split("/")[1]
        name = builder.split("/")[0]
        if not records.get(name):
            records[name] = []

        records[name].append(report.fetch_records_by_ids([tid]))

    for name, test_record in records.items():
        for tests in test_record:
            for full_id, test in tests.items():
                console.rule(f"[cyan]{name}/{full_id}")

                console.print(f"[blue]Executor: {test['executor']}")
                console.print(f"[blue]Description: {test['description']}")
                console.print(f"[blue]State: {test['state']}")
                console.print(f"[blue]Returncode: {test['returncode']}")
                console.print(f"[green]Runtime: {test['runtime']} sec")
                console.print(f"[green]Starttime: {test['starttime']}")
                console.print(f"[green]Endtime: {test['endtime']}")
                console.print(f"[green]Command: {test['command']}")
                console.print(f"[red]Test Script: {test['testpath']}")
                console.print(f"[red]Build Script: {test['build_script']}")
                console.print(f"[red]Output File: {test['outfile']}")
                console.print(f"[red]Error File: {test['errfile']}")
                console.print(f"[red]Log File: {test['logpath']}")

                if test["metrics"]:
                    table = Table("[blue]Name", "[blue]Value", title="Metrics")
                    for name, values in test["metrics"].items():
                        table.add_row(name, values)

                    console.print(table)

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

    query_builders = fetch_test_names(report=report, names=names)
    records = {}

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
