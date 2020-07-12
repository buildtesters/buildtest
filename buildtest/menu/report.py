import json
import os
import sys
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

    print(
        "{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format(
            "name",
            "state",
            "returncode",
            "starttime",
            "endtime",
            "runtime",
            "buildid",
            "buildspec",
        )
    )

    for buildspec in report.keys():
        for name in report[buildspec].keys():
            for test in report[buildspec][name]:
                print(
                    "{:<20} {:<20} {:<20} {:<20} {:<20} {:06.2f} {:<20} {:<20}".format(
                        name,
                        test["state"],
                        test["returncode"],
                        test["starttime"],
                        test["endtime"],
                        test["runtime"],
                        test["build_id"],
                        buildspec,
                    )
                )


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
            "build_id",
            "testroot",
            "testpath",
            "command",
            "outfile",
            "errfile",
            "schemafile",
            "executor",
        ]:
            entry[item] = builder.metadata[item]

        # query over result attributes, we only assign some keys of interest
        for item in ["starttime", "endtime", "runtime", "state", "returncode"]:
            entry[item] = builder.metadata["result"][item]

        report[buildspec][name].append(entry)

    with open(BUILD_REPORT, "w") as fd:
        json.dump(report, fd, indent=2)
