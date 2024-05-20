"""This module implements methods for buildtest inspect command that can be used
to retrieve test record from report file in JSON format."""

import re
import sys

from rich.pretty import pprint
from rich.table import Column, Table

from buildtest.defaults import console
from buildtest.utils.file import resolve_path
from buildtest.utils.print import print_file_content
from buildtest.utils.table import create_table, print_table, print_terse_format
from buildtest.utils.tools import checkColor


def print_by_query(
    report,
    name,
    theme=None,
    output=None,
    error=None,
    testpath=None,
    buildscript=None,
    buildenv=None,
):
    """This method prints the test records when they are queried using ``buildtest inspect query`` command.

    Args:
        report (buildtest.cli.report.Report): An instance of Report class
        name (list): List of test names to query
        theme (str, optional): Specify pygments theme for syntax highlighting
        output (bool, optional): Print output file when set to True
        error (bool, optional): Print error file when set to True
        testpath (bool, optional): Print testpath when set to True
        buildscript (bool, optional): Print buildscript when set to True
        buildenv (bool, optional): Print buildenv when set to True
    """

    records = {}
    query_builders = fetch_test_names(report, name)

    for builder in query_builders:
        tid = builder.split("/")[1]
        name = builder.split("/")[0]
        if not records.get(name):
            records[name] = []

        records[name].append(report.fetch_records_by_ids([tid]))

    for name, test_record in records.items():
        for tests in test_record:
            for full_id, test in tests.items():
                theme = theme or "monokai"

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
                    table = Table(
                        Column("Name", overflow="fold", header_style="blue"),
                        Column("Value", overflow="fold", header_style="blue"),
                        title="Metrics",
                    )
                    for name, values in test["metrics"].items():
                        table.add_row(name, values)

                    console.print(table)

                # print content of output file when 'buildtest inspect query --output' is set
                if output:
                    print_file_content(test["outfile"], "Output File: ", "text", theme)

                # print content of error file when 'buildtest inspect query --error' is set
                if error:
                    print_file_content(test["errfile"], "Error File: ", "text", theme)

                # print content of testpath when 'buildtest inspect query --testpath' is set
                if testpath:
                    print_file_content(test["testpath"], "Test File: ", "shell", theme)

                # print content of build script when 'buildtest inspect query --buildscript' is set
                if buildscript:
                    print_file_content(
                        test["build_script"], "Build Script File: ", "shell", theme
                    )

                if buildenv:
                    print_file_content(test["buildenv"], "Test File: ", "text", theme)


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


def print_builders(report, pager=None, color=None):
    """This method prints all the builders.

    Args:
        report (str): Path to report file
    """

    if pager:
        with console.pager():
            for name in report.builder_names():
                console.print(name)
        return

    for name in report.builder_names():
        console.print(f"[{color}]{name}")


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
        print_builders(report, pager=pager, color=consoleColor)
        return

    tdata = []

    for identifier in test_ids.keys():
        tdata.append(
            [
                identifier,
                test_ids[identifier]["name"],
                test_ids[identifier]["buildspec"],
            ]
        )

    # print output in terse format
    if terse:
        print_terse_format(
            tdata=tdata,
            headers=["id", "name", "buildspec"],
            color=consoleColor,
            display_header=no_header,
            pager=pager,
        )
        return

    # Create the table using the create_table method
    inspect_table = create_table(
        data=tdata,
        title="Test Summary by id, name, buildspec",
        columns=["id", "name", "buildspec"],
        header_style="blue",
        column_style=consoleColor,
    )

    print_table(inspect_table, pager=pager)


def inspect_query(
    report,
    name,
    theme=None,
    output=None,
    error=None,
    testpath=None,
    buildscript=None,
    buildenv=None,
    pager=None,
):
    """Entry point for ``buildtest inspect query`` command.

    Args:
        report (buildtest.cli.report.Report): An instance of Report class
        name (list): List of test names to query
        theme (str, optional): Specify pygments theme for syntax highlighting
        output (bool, optional): Print output file when set to True
        error (bool, optional): Print error file when set to True
        testpath (bool, optional): Print testpath when set to True
        buildscript (bool, optional): Print buildscript when set to True
        buildenv (bool, optional): Print buildenv when set to True
        pager (bool, optional): Print output in paging format
    """

    if pager:
        with console.pager():
            print_by_query(
                report,
                name=name,
                theme=theme,
                output=output,
                error=error,
                testpath=testpath,
                buildscript=buildscript,
                buildenv=buildenv,
            )
        return

    print_by_query(
        report,
        name=name,
        theme=theme,
        output=output,
        error=error,
        testpath=testpath,
        buildscript=buildscript,
        buildenv=buildenv,
    )


def inspect_buildspec(report, input_buildspecs, all_records=None, pager=None):
    """This method implements command ``buildtest inspect buildspec``

    Args:
        report (buildtest.cli.report.Report): An instance of Report class
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
        report (buildtest.cli.report.Report): An instance of Report class
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
        report (buildtest.cli.report.Report): An instance of Report class
        names (list): List of test names to search in report file. This is specified as positional arguments to ``buildtest inspect name``
        pager (bool, optional): Print output in paging format
    """

    if pager:
        with console.pager():
            print_by_name(report, names)
        return

    print_by_name(report, names)
