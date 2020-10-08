import json
import os
import sys
from tabulate import tabulate
from buildtest.defaults import BUILD_REPORT
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import is_file, create_dir, resolve_path


def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True


def func_report(args=None):

    # raise error if BUILD_REPORT not found
    if not is_file(BUILD_REPORT):
        sys.exit(f"Unable to fetch report no such file found: {BUILD_REPORT}")

    report = None
    with open(BUILD_REPORT, "r") as fd:
        report = json.loads(fd.read())

    # if report is None or issue with how json.load returns content of file we
    # raise error
    if not report:
        sys.exit(
            f"Fail to process {BUILD_REPORT} please check if file is valid json"
            f"or remove file"
        )

    # all format fields available for --helpformat
    format_fields = [
        "buildspec",
        "name",
        "id",
        "full_id",
        "testroot",
        "testpath",
        "command",
        "outfile",
        "errfile",
        "schemafile",
        "executor",
        "tags",
        "starttime",
        "endtime",
        "runtime",
        "state",
        "returncode",
    ]
    # generate help format table for printing purposes
    format_table = [
        ["buildspec", "Buildspec file"],
        ["name", "Name of test defined in buildspec"],
        ["id", "Unique Build Identifier (abbreviated)"],
        ["full_id", "Full qualified unique build identifier"],
        ["testroot", "Root of test directory"],
        ["testpath", "Path to test"],
        ["command", "Command executed"],
        ["outfile", "Output file"],
        ["errfile", "Error File"],
        ["schemafile", "Schema file used for validation"],
        ["executor", "Executor name"],
        ["tags", "Tag name"],
        ["starttime", "Start Time of test in date format"],
        ["endtime", "End Time for Test in date format"],
        ["runtime", "Total runtime in seconds"],
        ["state", "Test State reported by buildtest (PASS/FAIL)"],
        ["returncode", "Return Code from Test Execution"],
    ]
    # implements buildtest report --helpformat
    if args.helpformat:

        print(
            tabulate(format_table, headers=["Fields", "Description"], tablefmt="simple")
        )
        return

    filter_field_table = [
        ["buildspec", "Filter by buildspec file", "FILE"],
        ["name", "Filter by test name", "STRING"],
        ["executor", "Filter by executor name", "STRING"],
        ["state", "Filter by test state ", "PASS/FAIL"],
        ["tags", "Filter tests by tag name ", "STRING"],
        ["returncode", "Filter tests by returncode ", "INT"],
    ]
    filter_fields = ["buildspec", "name", "executor", "state", "tags", "returncode"]
    # filter_args contains a dict of filter field argument
    filter_args = {}

    # implements buildtest report --helpfilter
    if args.helpfilter:
        print(
            tabulate(
                filter_field_table,
                headers=["Filter Fields", "Description", "Expected Value"],
                tablefmt="simple",
            )
        )
        return

    # check if filter arguments (--filter) are valid fields
    if args.filter:

        filter_args = args.filter
        raiseError = False
        # check if filter keys are accepted filter fields, if not we raise error
        for key in filter_args.keys():
            if key not in filter_fields:
                print(f"Invalid filter key: {key}")
                raiseError = True

            if key == "returncode":
                valid_returncode = is_int(filter_args[key])

                if not valid_returncode:
                    raise BuildTestError(
                        f"Invalid returncode:{filter_args[key]} must be an integer"
                    )

        # raise error if any filter field is invalid
        if raiseError:
            sys.exit(1)

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

    fields = display_table.keys()

    # if buildtest report --format specified split field by "," and validate each
    # format field and reassign display_table
    if args.format:
        fields = args.format.split(",")

        # check all input format fields are valid fields
        for field in fields:
            if field not in format_fields:
                sys.exit(f"Invalid format field: {field}")

        # reassign display_table to format fields
        display_table = {}

        for field in fields:
            display_table[field] = []

    filter_buildspecs = report.keys()

    # This section filters the buildspec, if its invalid file or not found in cache
    # we raise error, otherwise we set filter_buildspecs to the filter argument 'buildspec'
    if filter_args.get("buildspec"):
        # resolve path for buildspec filter key, its possible if file doesn't exist method returns None
        resolved_buildspecs = resolve_path(filter_args["buildspec"])

        # if file doesn't exist we terminate with message
        if not resolved_buildspecs:
            print(
                f"Invalid File Path for filter field 'buildspec': {filter_args['buildspec']}"
            )
            sys.exit(0)

        # if file not found in cache we exit
        if not resolved_buildspecs in report.keys():
            print(f"buildspec file: {resolved_buildspecs} not found in cache")
            sys.exit(0)

        # need to set as a list since we will loop over all tests
        filter_buildspecs = [resolved_buildspecs]

    # ensure 'state' field in filter is either 'PASS' or 'FAIL', if not raise error
    if filter_args.get("state"):
        if filter_args["state"] not in ["PASS", "FAIL"]:
            print(
                f"filter argument 'state' must be 'PASS' or 'FAIL' got value {filter_args['state']}"
            )
            sys.exit(0)

    # process all filtered buildspecs and add rows to display_table.
    # filter_buildspec is either all buildspec or a single buildspec if
    # 'buildspec' filter field was set
    for buildspec in filter_buildspecs:

        # process each test in buildspec file
        for name in report[buildspec].keys():

            if filter_args.get("name"):
                # skip tests that don't equal filter 'name' field
                if name != filter_args["name"]:
                    continue

            # process all tests for an associated script. There can be multiple
            # test runs for a single test depending on how many tests were run
            for test in report[buildspec][name]:

                # filter by tags, if filter tag not found in test tag list we skip test
                if filter_args.get("tags"):
                    if filter_args["tags"] not in test.get("tags"):
                        continue

                # if 'executor' filter defined, skip test that don't match executor key
                if filter_args.get("executor"):
                    if filter_args.get("executor") != test.get("executor"):
                        continue

                # if state filter defined, skip any tests that don't match test state
                if filter_args.get("state"):
                    if filter_args["state"] != test.get("state"):
                        continue

                # if returncode filter defined, skip any tests that don't match returncode
                if filter_args.get("returncode"):
                    if int(filter_args["returncode"]) != test.get("returncode"):
                        continue

                if "buildspec" in display_table.keys():
                    display_table["buildspec"].append(buildspec)

                if "name" in display_table.keys():
                    display_table["name"].append(name)

                for field in fields:
                    # skip fields buildspec or name since they are accounted above and not part
                    # of test dictionary
                    if field in ["buildspec", "name"]:
                        continue

                    display_table[field].append(test[field])

    print(tabulate(display_table, headers=display_table.keys(), tablefmt="grid"))


def update_report(valid_builders):
    """This method will update BUILD_REPORT after every test run performed
       by ``buildtest build``. If BUILD_REPORT is not created, we will create
       file and update json file by extracting contents from builder.metadata

       :param valid_builders: builder object that were successful during build and able to execute test
       :type valid_builders: instance of BuilderBase (subclass)
    """

    if not is_file(os.path.dirname(BUILD_REPORT)):
        create_dir(os.path.dirname(BUILD_REPORT))

    # if file exists, read json file otherwise set report to empty dict
    try:
        with open(BUILD_REPORT, "r") as fd:
            report = json.loads(fd.read())
    except OSError:
        report = {}

    for builder in valid_builders:
        buildspec = builder.metadata["buildspec"]
        name = builder.metadata["name"]
        entry = {}

        report[buildspec] = report.get(buildspec) or {}
        report[buildspec][name] = report.get(buildspec, {}).get(name) or []

        # query over attributes found in builder.metadata, we only assign
        # keys that we care obout for reporting
        for item in [
            "id",
            "full_id",
            "testroot",
            "testpath",
            "command",
            "outfile",
            "errfile",
            "schemafile",
            "executor",
        ]:
            entry[item] = builder.metadata[item]

        entry["tags"] = ""
        # convert tags to string if defined in buildspec
        if builder.metadata["tags"]:
            if isinstance(builder.metadata["tags"], list):
                entry["tags"] = " ".join(builder.metadata["tags"])
            else:
                entry["tags"] = builder.metadata["tags"]

        # query over result attributes, we only assign some keys of interest
        for item in ["starttime", "endtime", "runtime", "state", "returncode"]:
            entry[item] = builder.metadata["result"][item]

        report[buildspec][name].append(entry)

    with open(BUILD_REPORT, "w") as fd:
        json.dump(report, fd, indent=2)
