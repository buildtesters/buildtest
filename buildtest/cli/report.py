import logging
import os
import sys

from buildtest.defaults import BUILD_REPORT, BUILDTEST_REPORT_SUMMARY
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import is_file, load_json, read_file, resolve_path
from tabulate import tabulate
from termcolor import colored

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
        "metrics",
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
        self,
        report_file=None,
        filter_args=None,
        format_args=None,
        latest=None,
        oldest=None,
    ):
        self.latest = latest
        self.oldest = oldest
        self.filter = filter_args
        self.format = format_args
        self.input_report = report_file

        # if no report set we read the default report file
        if report_file:
            self._reportfile = resolve_path(report_file)
        else:
            self._reportfile = BUILD_REPORT

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

        if not self._reportfile:
            sys.exit(f"Unable to resolve path to report file: {self.input_report}")

        if not is_file(self._reportfile):
            sys.exit(
                f"Unable to find report please check if {self._reportfile} is a file"
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
        """Filters test by ``executor`` property given input parameter ``buildtest report --filter executor:<executor>``. If there is a match
        we return ``True`` otherwise returns ``False``.

        :param test: name of test
        :type test: dict
        """
        if self.filter.get("executor") and self.filter.get("executor") != test.get(
            "executor"
        ):
            return True

        return False

    def _filter_by_state(self, test):
        """This method filters test by ``state`` property based on input parameter ``buildtest report --filter state:<STATE>``. If there is a match we
        return ``True`` otherwise returns ``False``.

        :param test: name of test
        :type test: dict
        """
        if self.filter.get("state") and self.filter.get("state") != test.get("state"):
            return True

        return False

    def _filter_by_returncode(self, test):
        """Returns True/False if test is filtered by returncode. We will get input returncode in filter field via ``buildtest report --filter returncode:<CODE>`` with
        one in test and if there is a match we return ``True`` otherwise returns ``False``.

        :param test: name of test
        :type test: dict
        """

        if self.filter.get("returncode"):
            if int(self.filter["returncode"]) != int(test.get("returncode")):
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
            ["metrics", "List all metrics if applicable"],
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
        """Displays list of help filters which implements command ``buildtest report --helpfilter``"""

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

    def print_report(self, terse=None, noheader=None):

        # if --terse option is specified we print output separated by PIPE symbol (|). Shown below is an example output

        # $ buildtest report --filter name=pbs_sleep --terse --format name,runtime
        # name|runtime
        # pbs_sleep|30.156192

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

    def latest_testid_by_name(self, name):
        """Given a test name return test id of latest run"""

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
        return self.filtered_buildspecs

    def get_testids(self):
        """Return a list of test ids from the report file"""

        id_lookup = self._testid_lookup()
        return list(id_lookup.keys())

    def _testid_lookup(self):
        """Return a dict in the format
        ```
        {
          <test-id>:
            {
              'name': <name test>
              'buildspec': <buildspec>
            }
           ...
        }
        ```
        """

        test_ids = {}
        for buildspec in self.filtered_buildspecs:
            # process each test in buildspec file
            for name in self.report[buildspec].keys():
                for test in self.report[buildspec][name]:
                    test_ids[test["full_id"]] = {"name": name, "buildspec": buildspec}

        return test_ids

    def builder_names(self):
        builders = []
        lookup = self._testid_lookup()
        for uid in lookup.keys():
            builders.append(lookup[uid]["name"] + "/" + uid)
        return builders

    def breakdown_by_test_names(self):
        """Returns a dictionary with number of test runs by testname"""
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
        records = {}

        for buildspec in self.filtered_buildspecs:
            for test in self.report[buildspec].keys():
                for test_record in self.report[buildspec][test]:
                    for identifier in testids:
                        if test_record["full_id"] == identifier:
                            records[identifier] = test_record

        return records


def report_cmd(args):

    if args.report_subcommand == "clear":
        if not is_file(args.report):
            sys.exit(f"There is no report file: {args.report} to delete")
        print(f"Removing report file: {args.report}")
        os.remove(BUILD_REPORT)
        return

    if args.report_subcommand == "list":
        if not is_file(BUILDTEST_REPORT_SUMMARY):
            print(
                "There are no report files, please run 'buildtest build' to generate a report file."
            )
            return

        content = read_file(BUILDTEST_REPORT_SUMMARY)
        print(content)
        return

    results = Report(
        filter_args=args.filter,
        format_args=args.format,
        latest=args.latest,
        oldest=args.oldest,
        report_file=args.report,
    )
    if args.report_subcommand == "summary":
        report_summary(results)
        return

    if args.helpfilter:
        results.print_filter_fields()
        return

    if args.helpformat:
        results.print_format_fields()
        return

    if not args.terse:
        print(f"Reading report file: {results.reportfile()} \n")

    results.print_report(terse=args.terse, noheader=args.no_header)


def report_summary(report):
    """Implements ``buildtest report summary``"""

    print("Report: ", report.reportfile())
    print("Total Tests:", len(report.get_testids()))
    print("Total Tests by Names: ", len(report.get_names()))
    print("Number of buildspecs in report: ", len(report.get_buildspecs()))

    test_breakdown = report.breakdown_by_test_names()

    table = {"name": [], "runs": [], "pass": [], "fail": []}
    for k in test_breakdown.keys():
        table["name"].append(k)
        table["runs"].append(test_breakdown[k]["runs"])
        table["pass"].append(test_breakdown[k]["pass"])
        table["fail"].append(test_breakdown[k]["fail"])

    headers = list(table.keys())

    print("\n")
    print("{:<20}".format(""), "Breakdown by Test")
    if os.getenv("BUILDTEST_COLOR") == "True":
        headers = [colored(field, "blue", attrs=["bold"]) for field in headers]

    print(tabulate(table, headers=headers, tablefmt="grid"))

    print("\n")
    print("{:<40}".format(""), "FAIL test")
    results = Report(
        filter_args={"state": "FAIL"},
        format_args="name,id,executor,state,returncode,runtime",
        report_file=report.reportfile(),
    )
    results.print_report()
