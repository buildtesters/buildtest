import json
import os
import sys
from tabulate import tabulate
from buildtest.defaults import BUILD_REPORT
from buildtest.utils.file import is_file, create_dir


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
        ["id", "Unique Build Identifier"],
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

    # default table format fields
    display_table = {
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
    # format field and generate display_table
    if args.format:
        fields = args.format.split(",")

        # check all input format fields are valid fields
        for field in fields:
            if field not in format_fields:
                sys.exit(f"Invalid format field: {field}")

        display_table = {}

        for field in fields:
            display_table[field] = []

    for buildspec in report.keys():
        for name in report[buildspec].keys():
            for test in report[buildspec][name]:

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

       Parameters

       :param valid_builders: builder object that were successful during build and able to execute test
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
            entry["tags"] = " ".join(builder.metadata["tags"])

        # query over result attributes, we only assign some keys of interest
        for item in ["starttime", "endtime", "runtime", "state", "returncode"]:
            entry[item] = builder.metadata["result"][item]

        report[buildspec][name].append(entry)

    with open(BUILD_REPORT, "w") as fd:
        json.dump(report, fd, indent=2)
