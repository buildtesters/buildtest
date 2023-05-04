"""This module implements methods for buildtest inspect command that can be used
to retrieve test record from report file in JSON format."""
import re
import sys

from buildtest.cli.report import Report
from buildtest.defaults import console
from buildtest.utils.file import read_file, resolve_path
from buildtest.utils.tools import checkColor
from rich.pretty import pprint
from rich.syntax import Syntax
from rich.table import Table


def inspect_cmd(args, report_file=None):
    """Entry point for ``buildtest inspect`` command

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
    """

    report = Report(report_file)

    # implements command 'buildtest inspect list'
    if args.inspect in ["list", "l"]:
        inspect_list(
            report,
            terse=args.terse,
            no_header=args.no_header,
            builder=args.builder,
            color=args.color,
            pager=args.pager,
            row_count=args.row_count,
        )
        return

    # implements command 'buildtest inspect name'
    if args.inspect in ["name", "n"]:
        inspect_by_name(report, args.name, args.pager)
        return

    if args.inspect in ["query", "q"]:
        inspect_query(report, args, args.pager)
        return

    if args.inspect in ["buildspec", "b"]:
        inspect_buildspec(
            report,
            input_buildspecs=args.buildspec,
            all_records=args.all,
            pager=args.pager,
        )


def fetch_test_names(report, names):
    """Return a list of builders given input test names by search the report file for valid records. If test is found it will be returned as a builder name. If names
    are specified without test ID then we retrieve latest record for test name. If names are specified with ID we find the first matching test record.

    Args:
        report (buildtest.cli.report.Report): An instance of Report class
        names (list): A list of test names
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


def print_builders(report):
    """This method prints all the builders.

    Args:
        report (str): Path to report file
    """

    builders = report.builder_names()
    for name in builders:
        console.print(name)


def print_terse(table, no_header=None, console_color=None):
    """This method prints output of builders in terse mode which is run via command ``buildtest inspect list --terse``

    Args:
        table (dict): Table with columns required for the ``buildtest inspect list`` command.
        no_header (bool, optional): Determine whether to print header in terse format.
        console_color (bool, optional): Select desired color when displaying results
    """

    row_entry = [table[key] for key in table.keys()]
    transpose_list = [list(i) for i in zip(*row_entry)]

    # We print the table columns if --no-header is not specified
    if not no_header:
        console.print("|".join(table.keys()), style=console_color)

    for row in transpose_list:
        console.print("|".join(row), style=console_color)


def inspect_list(
    report,
    terse=None,
    no_header=None,
    builder=None,
    color=None,
    pager=None,
    row_count=None,
):
    """This method list an output of test id, name, and buildspec file from the report cache. The default
    behavior is to display output in table format though this can be changed with terse format which will
    display in parseable format. This method implements command ``buildtest inspect list``

    Args:
        report (str): Path to report file
        terse (bool, optional): Print output in terse format
        no_header (bool, optional): Determine whether to print header in terse format.
        builder (bool, optional): Print output in builder format which can be done via ``buildtest inspect list --builder``
        color (bool, optional): Print table output of ``buildtest inspect list`` with selected color
        pager (bool, optional): Print output in paging format
        row_count (bool, optional): Print total number of test runs
    """
    consoleColor = checkColor(color)

    test_ids = report._testid_lookup()

    if row_count:
        print(len(test_ids))
        return

    # implement command 'buildtest inspect list --builder'
    if builder:
        if pager:
            with console.pager():
                print_builders(report)
            return

        print_builders(report)
        return

    table = {
        "id": [],
        "name": [],
        "buildspec": [],
    }

    for identifier in test_ids.keys():
        table["id"].append(identifier)
        table["name"].append(test_ids[identifier]["name"])
        table["buildspec"].append(test_ids[identifier]["buildspec"])

    # print output in terse format
    if terse:
        if pager:
            with console.pager():
                print_terse(table, no_header, consoleColor)
            return

        print_terse(table, no_header, consoleColor)
        return

    inspect_table = Table(
        header_style="blue",
        title="Test Summary by id, name, buildspec",
        row_styles=[consoleColor],
    )
    for column in table.keys():
        inspect_table.add_column(column)

    for identifier, name, buildspec in zip(
        table["id"], table["name"], table["buildspec"]
    ):
        inspect_table.add_row(identifier, name, buildspec)

    if pager:
        with console.pager():
            console.print(inspect_table)
        return

    console.print(inspect_table)


def print_by_query(report, args):
    """This method prints the test records when they are queried using ``buildtest inspect query`` command.

    Args:
        report (str): Path to report file
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
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
                theme = args.theme or "monokai"

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

                    syntax = Syntax(content, "text", theme=theme)
                    console.print(syntax)

                # print content of testpath when 'buildtest inspect query --testpath' is set
                if args.testpath:
                    content = read_file(test["testpath"])
                    console.rule(f"Test File: {test['testpath']}")

                    syntax = Syntax(content, "shell", theme=theme)
                    console.print(syntax)

                # print content of build script when 'buildtest inspect query --buildscript' is set
                if args.buildscript:
                    content = read_file(test["build_script"])
                    console.rule(f"Test File: {test['build_script']}")

                    syntax = Syntax(content, lexer="shell", theme=theme)
                    console.print(syntax)

                if args.buildenv:
                    content = read_file(test["buildenv"])
                    console.rule(f"Test File: {test['buildenv']}")

                    syntax = Syntax(content, lexer="text", theme=theme)
                    console.print(syntax)


def inspect_query(report, args, pager=None):
    """Entry point for ``buildtest inspect query`` command.

    Args:
        report (str): Path to report file
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
        pager (bool, optional): Print output in paging format
    """

    if pager:
        with console.pager():
            print_by_query(report, args)
        return

    print_by_query(report, args)


def inspect_buildspec(report, input_buildspecs, all_records, pager=None):
    """This method implements command ``buildtest inspect buildspec``

    Args:
        report (str): Path to report file
        input_buildspecs (list): List of buildspecs to search in report file. This is specified as positional arguments to ``buildtest inspect buildspec``
        all_records (bool): Determine whether to display all records for every test that matches the buildspec. By default we retrieve the latest record.
        pager (bool, optional): Print output in paging format
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

    if pager:
        with console.pager():
            console.print(records)
        return

    pprint(records)


def print_by_name(report, names):
    """This method prints test records by given name in JSON format.

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

    console.print(records)


def inspect_by_name(report, names, pager=None):
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
        pager (bool, optional): Print output in paging format
    """

    if pager:
        with console.pager():
            print_by_name(report, names)
        return

    print_by_name(report, names)
    return
