import logging
import os
import sys

from tabulate import tabulate
from termcolor import colored

from buildtest.defaults import BUILD_REPORT
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import is_file, load_json, resolve_path

logger = logging.getLogger(__name__)


def is_int(val):

    try:
        int(val)
    except ValueError:
        return False
    return True


class Report:
    # list of format fields
    format_fields = [
        "buildspec",
        "command",
        "compiler",
        "endtime",
        "errfile",
        "executor",
        "full_id",
        "hostname",
        "id",
        "name",
        "outfile",
        "runtime",
        "returncode",
        "schemafile",
        "starttime",
        "state",
        "tags",
        "testroot",
        "testpath",
        "user",
    ]
    # list of filter fields
    filter_fields = ["buildspec", "name", "executor", "state", "tags", "returncode"]

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
        self, filter_args, format_args, latest, oldest, report_file=BUILD_REPORT
    ):
        self.latest = latest
        self.oldest = oldest
        self.filter = filter_args
        self.format = format_args
        self.reportfile = resolve_path(report_file)
        self.report = self.load()
        self._check_filter_fields()
        self._check_format_fields()
        self.filter_buildspecs_from_report()

        self.process_report()

    def get_report_file(self):
        return self.reportfile

    def _check_filter_fields(self):
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
        is loaded using ``json.loads`` and return value is a dictionary containing
        entire report of all tests.
        """

        if not is_file(self.reportfile):
            sys.exit(f"Unable to fetch report no such file found: {self.reportfile}")

        report = load_json(self.reportfile)

        logger.debug(f"Loading report file: {self.reportfile}")

        # if report is None or issue with how json.load returns content of file we
        # raise error
        if not report:
            sys.exit(
                f"Fail to process {self.reportfile} please check if file is valid json"
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
                print(
                    f"Invalid File Path for filter field 'buildspec': {self.filter['buildspec']}"
                )
                sys.exit(0)

            # if file not found in cache we exit
            if not resolved_buildspecs in self.report.keys():
                print(f"buildspec file: {resolved_buildspecs} not found in cache")
                sys.exit(0)

            # need to set as a list since we will loop over all tests
            self.filtered_buildspecs = [resolved_buildspecs]

        # ensure 'state' field in filter is either 'PASS' or 'FAIL', if not raise error
        if self.filter.get("state"):
            if self.filter["state"] not in ["PASS", "FAIL"]:
                print(
                    f"filter argument 'state' must be 'PASS' or 'FAIL' got value {self.filter['state']}"
                )
                sys.exit(0)

    def _filter_by_names(self, name):
        """Filter test by name of test. This method will return True if record should be processed,
        otherwise returns False

        :param name: Name of test
        :type name: str
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

        :param test: test record
        :type test: dict
        :return: Return True if test is filtered out, otherwise return False
        :rtype: bool
        """

        if self.filter.get("tags") and self.filter.get("tags") not in test.get("tags"):
            return True

        return False

    def _filter_by_executor(self, test):

        if self.filter.get("executor") and self.filter.get("executor") != test.get(
            "executor"
        ):
            return True

        return False

    def _filter_by_state(self, test):

        if self.filter.get("state") and self.filter.get("state") != test.get("state"):
            return True

        return False

    def _filter_by_returncode(self, test):

        if self.filter.get("returncode"):
            if int(self.filter["returncode"]) != test.get("returncode"):
                return True

        return False

    def process_report(self):
        # process all filtered buildspecs and add rows to display_table.
        # filter_buildspec is either all buildspec or a single buildspec if
        # 'buildspec' filter field was set

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
                        self.display_table[field].append(test[field])

    def print_format_fields(self):
        """Implements command ``buildtest report --helpformat``"""
        format_table = [
            ["buildspec", "Buildspec file"],
            ["command", "Command executed"],
            [
                "compiler",
                "Retrieve compiler used for test (applicable for compiler schema)",
            ],
            ["endtime", "End Time for Test in date format"],
            ["errfile", "Error File"],
            ["executor", "Executor name"],
            ["hostname", "Retrieve hostname of machine where job was submitted from"],
            ["full_id", "Full qualified unique build identifier"],
            ["id", "Unique Build Identifier (abbreviated)"],
            ["name", "Name of test defined in buildspec"],
            ["outfile", "Output file"],
            ["returncode", "Return Code from Test Execution"],
            ["runtime", "Total runtime in seconds"],
            ["schemafile", "Schema file used for validation"],
            ["starttime", "Start Time of test in date format"],
            ["state", "Test State reported by buildtest (PASS/FAIL)"],
            ["tags", "Tag name"],
            ["testroot", "Root of test directory"],
            ["testpath", "Path to test"],
            ["user", "Get user who submitted job"],
        ]

        headers = ["Fields", "Description"]
        table = []
        if os.getenv("BUILDTEST_COLOR") == "True":
            # color first column green and second column red
            for row in format_table:
                table.append(
                    [colored(row[0], "green", attrs=["bold"]), colored(row[1], "red")]
                )

            print(
                tabulate(
                    table,
                    headers=[
                        colored(field, "blue", attrs=["bold"]) for field in headers
                    ],
                    tablefmt="simple",
                )
            )
            return

        print(tabulate(format_table, headers=headers, tablefmt="simple"))

    def print_filter_fields(self):
        """Implements command ``buildtest report --helpfilter``"""

        filter_field_table = [
            ["buildspec", "Filter by buildspec file", "FILE"],
            ["name", "Filter by test name", "STRING"],
            ["executor", "Filter by executor name", "STRING"],
            ["state", "Filter by test state ", "PASS/FAIL"],
            ["tags", "Filter tests by tag name ", "STRING"],
            ["returncode", "Filter tests by returncode ", "INT"],
        ]
        headers = ["Filter Fields", "Description", "Expected Value"]
        table = []
        if os.getenv("BUILDTEST_COLOR") == "True":
            for row in filter_field_table:
                table.append(
                    [
                        colored(row[0], "green", attrs=["bold"]),
                        colored(row[1], "red"),
                        colored(row[2], "cyan"),
                    ]
                )
            print(
                tabulate(
                    table,
                    headers=[
                        colored(field, "blue", attrs=["bold"]) for field in headers
                    ],
                    tablefmt="simple",
                )
            )
            return

        print(tabulate(filter_field_table, headers=headers, tablefmt="simple"))

    def print_display_table(self):
        if os.getenv("BUILDTEST_COLOR") == "True":
            print(
                tabulate(
                    self.display_table,
                    headers=[
                        colored(field, "blue", attrs=["bold"])
                        for field in self.display_table.keys()
                    ],
                    tablefmt="grid",
                )
            )
            return

        print(
            tabulate(
                self.display_table, headers=self.display_table.keys(), tablefmt="grid"
            )
        )


def report_cmd(args):

    if args.report_subcommand == "clear":
        if not is_file(args.report):
            sys.exit(f"There is no report file: {args.report} to delete")
        print(f"Removing report file: {args.report}")
        os.remove(BUILD_REPORT)
        return

    results = Report(args.filter, args.format, args.latest, args.oldest, args.report)
    if args.helpfilter:
        results.print_filter_fields()
        return

    if args.helpformat:
        results.print_format_fields()
        return

    print(f"Reading report file: {results.get_report_file()} \n")
    results.print_display_table()
