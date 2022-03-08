import logging
import os
import sys

from buildtest.defaults import BUILD_REPORT, BUILDTEST_REPORTS, console
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import is_file, load_json, resolve_path
from rich.table import Table

logger = logging.getLogger(__name__)


def is_int(val):
    """Check if input is an integer by running `int() <https://docs.python.org/3/library/functions.html#int>`_. If its successful we
    return **True** otherwise returns **False**
    """

    try:
        int(val)
    except ValueError:
        return False
    return True


class Report:
    # list of format fields
    format_field_description = {
        "buildspec": "Buildspec File",
        "command": "Command executed",
        "compiler": "Retrieve compiler used for test (applicable for compiler schema)",
        "endtime": "End Time for test",
        "errfile": "Error File",
        "executor": "Name of executor used for running test",
        "hostname": "Hostname of machine where job was submitted from",
        "full_id": "Fully qualified build identifier",
        "id": "Unique build identifier",
        "metrics": "List all metrics for test",
        "name": "Name of test",
        "outfile": "Output file",
        "returncode": "Return Code",
        "runtime": "Total runtime in seconds",
        "schemafile": "Schema file used for validating test",
        "starttime": "Start time of test",
        "state": "State of test (PASS/FAIL)",
        "tags": "Tag name",
        "testroot": "Root of test directory",
        "testpath": "Path to test",
        "user": "User who ran the test",
    }
    filter_field_description = {
        "buildspec": {"description": "Filter by buildspec file", "type": "FILE"},
        "name": {"description": "Filter by test name", "type": "STRING"},
        "executor": {"description": "Filter by executor name", "type": "STRING"},
        "returncode": {"description": "Filter tests by returncode", "type": "INT"},
        "state": {"description": "Filter by test state", "type": "PASS/FAIL"},
        "tags": {"description": "Filter tests by tag name", "type": "STRING"},
    }

    format_fields = format_field_description.keys()
    # list of filter fields
    filter_fields = filter_field_description.keys()

    # default table format fields
    display_table = {
        "name": [],
        "id": [],
        "state": [],
        "returncode": [],
        "starttime": [],
        "endtime": [],
        "runtime": [],
        "tags": [],
        "buildspec": [],
    }

    def __init__(
        self,
        report_file=None,
        filter_args=None,
        format_args=None,
        latest=None,
        oldest=None,
        pager=None,
    ):
        """
        Args:
            report_file (str, optional): Full path to report file to read
            filter_args (str, optional): A comma separated list of Key=Value pair for filter arguments via ``buildtest report --filter``
            format (str, optional): A comma separated list of format fields for altering report table. This is specified via ``buildtest report --format``
            latest (bool, optional): Fetch latest run for all tests discovered. This is specified via ``buildtest report --latest``
            oldest (bool, optional): Fetch oldest run for all tests discovered. This is specified via ``buildtest report --oldest``
            pager (bool, optional): Enabling PAGING output for ``buildtest report``. This can be specified via ``buildtest report --pager``
        """
        self.latest = latest
        self.oldest = oldest
        self.filter = filter_args
        self.format = format_args
        self.pager = pager

        self.input_report = report_file

        # if no report specified use default report
        if not self.input_report:
            self._reportfile = BUILD_REPORT
        # otherwise honor report file specified on argument
        else:
            self._reportfile = resolve_path(report_file)

        self.report = self.load()
        self._check_filter_fields()
        self._check_format_fields()
        self.filter_buildspecs_from_report()

        self.process_report()

    def reportfile(self):
        """Return full path to report file"""
        return self._reportfile

    def get(self):
        """Return raw content of report file"""
        return self.report

    def _check_filter_fields(self):
        """This method will validate filter fields ``buildtest report --filter`` by checking if field is valid filter field. If one specifies
        an invalid filter field, we will raise an exception

        Raises:
            BuildTestError: Raise exception if its in invalid filter field. If returncode is not an integer we raise exception
        """

        # check if filter arguments (--filter) are valid fields
        if self.filter:

            logger.debug(f"Checking filter fields: {self.filter}")

            # check if filter keys are accepted filter fields, if not we raise error
            for key in self.filter.keys():
                if key not in self.filter_fields:
                    self.print_filter_fields()
                    raise BuildTestError(
                        f"Invalid filter key: {key}, please run 'buildtest report --helpfilter' for list of available filter fields"
                    )

                if key == "returncode" and not is_int(self.filter[key]):
                    raise BuildTestError(
                        f"Invalid returncode:{self.filter[key]} must be an integer"
                    )

                logger.debug(f"filter field: {key} is valid")

    def _check_format_fields(self):
        """Check all format arguments (--format) are valid, the arguments are specified
        in format (--format key1=val1,key2=val2). We make sure each key is valid
        format field.

        Raises:
            BuildTestError: If format field is not valid
        """

        self.display_format_fields = self.display_table.keys()

        # if buildtest report --format specified split field by "," and validate each
        # format field and reassign display_table
        if self.format:

            logger.debug(f"Checking format fields: {self.format}")

            self.display_format_fields = self.format.split(",")
            # check all input format fields are valid fields
            for field in self.display_format_fields:
                if field not in self.format_fields:
                    self.print_format_fields()
                    raise BuildTestError(f"Invalid format field: {field}")

            # reassign display_table to format fields
            self.display_table = {}

            for field in self.display_format_fields:
                self.display_table[field] = []

    def load(self):
        """This method is responsible for loading report file. If file not found
        or report is empty dictionary we raise an error. The report file
        is loaded if its valid JSON file and returns as  dictionary containing
        entire report of all tests.

        Raises:
            SystemExit: If report file doesn't exist or path is not a file. If the report file is empty upon loading we raise an error.
        """

        if not self._reportfile:
            sys.exit(
                console.print(
                    f"[red]Unable to resolve path to report file: {self.input_report}"
                )
            )

        if not is_file(self._reportfile):
            sys.exit(
                console.print(
                    f"Unable to find report please check if {self._reportfile} is a file or run a test via 'buildtest build' to generate report file"
                )
            )

        report = load_json(self._reportfile)

        logger.debug(f"Loading report file: {self._reportfile}")

        # if report is None or issue with how json.load returns content of file we
        # raise error
        if not report:
            sys.exit(
                f"Fail to process {self._reportfile} please check if file is valid json"
                f"or remove file"
            )
        return report

    def filter_buildspecs_from_report(self):
        """This method filters the report table input filter ``--filter buildspec``. If entry found in buildspec
        cache we add to list
        """

        # by default all keys from report are buildspec files to process
        self.filtered_buildspecs = self.report.keys()

        # if --filter option not specified we return from method
        if not self.filter:
            return

        if self.filter.get("buildspec"):
            # resolve path for buildspec filter key, its possible if file doesn't exist method returns None
            resolved_buildspecs = resolve_path(self.filter["buildspec"])

            logger.debug(f"Filter records by buildspec: {resolved_buildspecs}")

            # if file doesn't exist we terminate with message
            if not resolved_buildspecs:
                raise BuildTestError(
                    f"Invalid File Path for filter field 'buildspec': {self.filter['buildspec']}"
                )

            # if file not found in cache we exit
            if not resolved_buildspecs in self.report.keys():
                raise BuildTestError(
                    f"buildspec file: {resolved_buildspecs} not found in cache"
                )

            # need to set as a list since we will loop over all tests
            self.filtered_buildspecs = [resolved_buildspecs]

        # ensure 'state' field in filter is either 'PASS' or 'FAIL', if not raise error
        if self.filter.get("state"):
            if self.filter["state"] not in ["PASS", "FAIL"]:
                raise BuildTestError(
                    f"filter argument 'state' must be 'PASS' or 'FAIL' got value {self.filter['state']}"
                )

    def _filter_by_names(self, name):
        """Filter test by name of test. This method will return True if record should be processed,
        otherwise returns False

        Args:
            name (str): Name of test to filter
        """

        if not self.filter.get("name"):
            return False

        logger.debug(
            f"Checking if test: '{name}' matches filter name: '{self.filter['name']}'"
        )

        return not name == self.filter["name"]

    def _filter_by_tags(self, test):
        """This method will return a boolean (True/False) to check if test should be skipped from report. Given an input test, we
        check if test has 'tags' property in buildspec and if tagnames specified by ``--filter tags`` are found in the test. If
        there is a match we return ``False``. A ``True`` indicates the test will be filtered out.

        Args:
            test (dict): Test recorded loaded as dictionary
        """

        if self.filter.get("tags") and self.filter.get("tags") not in test.get("tags"):
            return True

        return False

    def _filter_by_executor(self, test):
        """Filters test by ``executor`` property given input parameter ``buildtest report --filter executor:<executor>``. If there is **no** match
        we return ``True`` otherwise returns ``False``.

        Args:
            test (dict): Test recorded loaded as dictionary
        """

        if self.filter.get("executor") and self.filter.get("executor") != test.get(
            "executor"
        ):
            return True

        return False

    def _filter_by_state(self, test):
        """This method filters test by ``state`` property based on input parameter ``buildtest report --filter state:<STATE>``. If there is **no**
        match we return ``True`` otherwise returns ``False``.

        Args:
            test (dict): Test recorded loaded as dictionary
        """
        if self.filter.get("state") and self.filter.get("state") != test.get("state"):
            return True

        return False

    def _filter_by_returncode(self, test):
        """Returns True/False if test is filtered by returncode. We will get input returncode in filter field via ``buildtest report --filter returncode:<CODE>`` with
        one in test and if there is a match we return ``True`` otherwise returns ``False``.

        Args:
            test (dict): Test recorded loaded as dictionary
        """

        if self.filter.get("returncode"):
            if int(self.filter["returncode"]) != int(test.get("returncode")):
                return True

        return False

    def process_report(self):
        # process all filtered buildspecs and add rows to display_table.
        for buildspec in self.filtered_buildspecs:

            # process each test in buildspec file
            for name in self.report[buildspec].keys():

                if self.filter:
                    if self._filter_by_names(name):
                        continue

                tests = self.report[buildspec][name]

                # if --latest and --oldest specified together we retrieve first and last record
                if self.latest and self.oldest:
                    tests = [
                        self.report[buildspec][name][0],
                        self.report[buildspec][name][-1],
                    ]
                # retrieve last record of every test if --latest is specified
                elif self.latest:
                    tests = [self.report[buildspec][name][-1]]
                # retrieve first record of every test if --oldest is specified
                elif self.oldest:
                    tests = [self.report[buildspec][name][0]]

                # process all tests for an associated script. There can be multiple
                # test runs for a single test depending on how many tests were run
                for test in tests:

                    if self.filter:
                        # filter by tags, if filter tag not found in test tag list we skip test
                        if self._filter_by_tags(test):
                            continue

                        # if 'executor' filter defined, skip test that don't match executor key
                        if self._filter_by_executor(test):
                            continue

                        # if state filter defined, skip any tests that don't match test state
                        if self._filter_by_state(test):
                            continue

                        # if returncode filter defined, skip any tests that don't match returncode
                        if self._filter_by_returncode(test):
                            continue

                    if "buildspec" in self.display_table.keys():
                        self.display_table["buildspec"].append(buildspec)

                    if "name" in self.display_table.keys():
                        self.display_table["name"].append(name)

                    for field in self.display_format_fields:
                        # skip fields buildspec or name since they are accounted above and not part
                        # of test dictionary
                        if field in ["buildspec", "name"]:
                            continue

                        # the metrics field is a dict, we will print output as a comma separated list of key/value pair
                        if field == "metrics":
                            msg = ""
                            for key, value in test[field].items():
                                msg += f"{key}={value},"
                            msg = msg.rstrip(",")

                            self.display_table[field].append(msg)
                        else:
                            self.display_table[field].append(test[field])

    def print_format_fields(self):
        """Displays list of format field which implements command ``buildtest report --helpformat``"""
        table = Table("[blue]Field", "[blue]Description", title="Format Fields")
        for field, description in self.format_field_description.items():
            table.add_row(f"[red]{field}", f"[green]{description}")

        console.print(table)

    def print_filter_fields(self):
        """Displays list of help filters which implements command ``buildtest report --helpfilter``"""

        table = Table(
            "[blue]Field",
            "[blue]Description",
            "[blue]Expected Value",
            title="Filter Fields",
        )

        for field, value in self.filter_field_description.items():
            table.add_row(
                f"[red]{field}",
                f"[green]{value['description']}",
                f"[magenta]{value['type']}",
            )
        console.print(table)

    def print_report(self, terse=None, noheader=None, title=None):
        """This method will print report table after processing report file. By default we print output in
        table format but this can be changed to terse format which will print output in parseable format.

        Args:
            terse (bool, optional): Print output int terse format
            noheader (bool, optional): Determine whether to print header in terse format


        In this example, we display output in tabular format which works with ``--filter`` and ``--format`` option.

        .. code-block:: console

            bash-3.2$ buildtest report --filter name=root_disk_usage --format name,state,returncode
            Reading report file: /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/report.json

            +-----------------+---------+--------------+
            | name            | state   |   returncode |
            +=================+=========+==============+
            | root_disk_usage | PASS    |            0 |
            +-----------------+---------+--------------+
            | root_disk_usage | PASS    |            0 |
            +-----------------+---------+--------------+
            | root_disk_usage | PASS    |            0 |
            +-----------------+---------+--------------+

        In terse format each output is separated by PIPE symbol (**|***). The first row contains headers followed by content of the report.

        .. code-block:: console

            bash-3.2$ buildtest report --filter name=root_disk_usage --format name,state,returncode --terse
            name|state|returncode
            root_disk_usage|PASS|0
            root_disk_usage|PASS|0
            root_disk_usage|PASS|0

        You can avoid printing the header table by specifying `--no-header` option

        .. code-block:: console

            bash-3.2$ buildtest report --filter name=root_disk_usage --format name,state,returncode --terse --no-header
            root_disk_usage|PASS|0
            root_disk_usage|PASS|0
            root_disk_usage|PASS|0
        """

        if terse:
            join_list = []

            for key in self.display_table.keys():
                join_list.append(self.display_table[key])

            t = [list(i) for i in zip(*join_list)]

            if not noheader:
                print("|".join(self.display_table.keys()))

            for i in t:
                print("|".join(i))

            return

        join_list = []
        title = title or f"Report File: {self.reportfile()}"
        table = Table(title=title, show_lines=True, expand=True)
        for field in self.display_table.keys():
            table.add_column(f"[blue]{field}", overflow="fold", style="red")
            join_list.append(self.display_table[field])

        transpose_list = [list(i) for i in zip(*join_list)]
        for row in transpose_list:
            table.add_row(*row)

        if self.pager:
            with console.pager():
                console.print(table)

            return
        console.print(table)
        return

    def latest_testid_by_name(self, name):
        """Given a test name return test id of latest run

        Args:
            name (str): Name of test to search in report file and retrieve corresponding test id
        """

        for buildspec in self.report.keys():
            if name not in self.report[buildspec].keys():
                continue

            return self.report[buildspec][name][-1].get("full_id")

    def get_names(self):
        """Return a list of test names from report file"""
        test_names = []
        for buildspec in self.filtered_buildspecs:
            # process each test in buildspec file
            for name in self.report[buildspec].keys():
                test_names.append(name)

        return test_names

    def get_buildspecs(self):
        """Return a list of buildspecs in report file"""
        return self.filtered_buildspecs

    def get_testids(self):
        """Return a list of test ids from the report file"""

        id_lookup = self._testid_lookup()
        return list(id_lookup.keys())

    def _testid_lookup(self):
        """Return a dict where `key` represents full id of test and value is a dictionary
        containing two values ``name`` and ``buildspec`` property which contains name of test
        and path to buildspec file.
        """

        test_ids = {}
        for buildspec in self.filtered_buildspecs:
            # process each test in buildspec file
            for name in self.report[buildspec].keys():
                for test in self.report[buildspec][name]:
                    test_ids[test["full_id"]] = {"name": name, "buildspec": buildspec}

        return test_ids

    def lookup(self):
        """Create a lookup dictionary with keys corresponding to name of test names and values are list of test ids.

        .. code-block:: python

            from buildtest.cli.report import Report
            r = Report()
            r.lookup()
            {'exit1_fail': ['913ce128-f425-488a-829d-d5d898113e8b', '54fc3dfe-50c5-4d2c-93fc-0c26364d215d', '70971081-84f9-462e-809b-a7d438a480bf'], 'exit1_pass': ['775a5545-bac5-468d-994d-85b22544306b', '0e908a64-fc81-4606-8ef4-78360563618e', '17082a05-ba32-4ef1-a38a-c2c6ea125bae', '3f50a73c-e333-4bbb-a722-aa5d72f98ac1', '964cd416-ad91-42be-bc1c-e25119f6df5d']}


        """
        builder = {}
        for buildspec in self.report.keys():
            for name in self.report[buildspec].keys():
                builder[name] = []
                for test in self.report[buildspec][name]:
                    builder[name].append(test["full_id"])

        return builder

    def builder_names(self):
        """Return a list of builder names in builder format which is in the form: `<NAME>/<TESTID>`."""
        builders = []
        lookup = self._testid_lookup()
        for uid in lookup.keys():
            builders.append(lookup[uid]["name"] + "/" + uid)
        return builders

    def breakdown_by_test_names(self):
        """Returns a dictionary with number of test runs, pass test and fail test by testname"""
        tests = {}
        for buildspec in self.filtered_buildspecs:
            for name in self.report[buildspec].keys():
                pass_tests = 0
                fail_tests = 0
                for test in self.report[buildspec][name]:
                    if test["state"] == "PASS":
                        pass_tests += 1
                    else:
                        fail_tests += 1

                tests[name] = {
                    "runs": len(self.report[buildspec][name]),
                    "pass": pass_tests,
                    "fail": fail_tests,
                }
        return tests

    def fetch_records_by_ids(self, testids):
        """Fetch a test record given a list of test identifier.

        Args:
            testids (list): A list of test IDs to search in report file and retrieve JSON record for each test.
        """
        records = {}

        for buildspec in self.filtered_buildspecs:
            for test in self.report[buildspec].keys():
                for test_record in self.report[buildspec][test]:
                    for identifier in testids:
                        if test_record["full_id"] == identifier:
                            records[identifier] = test_record

        return records


def report_cmd(args, report_file=None):
    """Entry point for ``buildtest report`` command"""

    if args.report_subcommand == "clear":
        # if BUILDTEST_REPORTS file is not present then we have no report files to delete since it tracks all report files that are created
        if not is_file(BUILDTEST_REPORTS):
            sys.exit("There is no report file to delete")

        reports = load_json(BUILDTEST_REPORTS)
        for report in reports:
            console.print(f"Removing report file: {report}")
            try:
                os.remove(report)
            except OSError:
                continue

        os.remove(BUILDTEST_REPORTS)
        return

    if args.report_subcommand == "list":
        if not is_file(BUILDTEST_REPORTS):
            sys.exit(
                console.print(
                    "There are no report files, please run 'buildtest build' to generate a report file."
                )
            )

        content = load_json(BUILDTEST_REPORTS)
        for fname in content:
            console.print(fname)
        return

    results = Report(
        filter_args=args.filter,
        format_args=args.format,
        latest=args.latest,
        oldest=args.oldest,
        report_file=report_file,
        pager=args.pager,
    )
    if args.report_subcommand == "summary":
        report_summary(results, args.pager)
        return

    if args.helpfilter:
        results.print_filter_fields()
        return

    if args.helpformat:
        results.print_format_fields()
        return

    results.print_report(terse=args.terse, noheader=args.no_header)


def report_summary(report, pager=None):
    """This method will print summary for report file which can be retrieved via ``buildtest report summary`` command"""

    test_breakdown = report.breakdown_by_test_names()

    table = Table(title="Breakdown by test", header_style="blue")
    table.add_column("Name", style="cyan")
    table.add_column("Total Pass", style="green")
    table.add_column("Total Fail", style="red")
    table.add_column("Total Runs", style="blue")
    for k in test_breakdown.keys():
        table.add_row(
            k,
            str(test_breakdown[k]["pass"]),
            str(test_breakdown[k]["fail"]),
            str(test_breakdown[k]["runs"]),
        )

    pass_results = Report(
        filter_args={"state": "PASS"},
        format_args="name,id,executor,state,returncode,runtime",
        report_file=report.reportfile(),
    )

    fail_results = Report(
        filter_args={"state": "FAIL"},
        format_args="name,id,executor,state,returncode,runtime",
        report_file=report.reportfile(),
    )
    if pager:
        with console.pager():
            print_report_summary_output(report, table, pass_results, fail_results)

        return

    print_report_summary_output(report, table, pass_results, fail_results)


def print_report_summary_output(report, table, pass_results, fail_results):
    """Print output of ``buildtest report summary``.

    Args:
        report (buildtest.cli.report.Report): An instance of Report class
        table (rich.table.Table): An instance of Rich Table class
        pass_results (buildtest.cli.report.Report): An instance of Report class with filtered output by ``state=PASS``
        fail_results (buildtest.cli.report.Report): An instance of Report class with filtered output by ``state=FAIL``
    """
    console.print("Report File: ", report.reportfile())
    console.print("Total Tests:", len(report.get_testids()))
    console.print("Total Tests by Names: ", len(report.get_names()))
    console.print("Number of buildspecs in report: ", len(report.get_buildspecs()))
    console.print(table)
    pass_results.print_report(title="PASS Tests")
    fail_results.print_report(title="FAIL Tests")
