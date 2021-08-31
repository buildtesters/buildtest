import sys

from buildtest.cli.report import Report
from buildtest.exceptions import BuildTestError


def path_cmd(
    name, testpath=None, outfile=None, errfile=None, buildscript=None, stagedir=None
):
    report = Report()

    tid = None
    builders = report.builder_names()

    # if input name contains a '/' followed by TEST ID we will match id
    if name.find("/") != -1:

        for builder in builders:
            if builder.startswith(name):
                tid = builder.split("/")[1]
                break

    else:
        tid = report.latest_testid_by_name(name)

    if not tid:
        print("Please select one of the following builders:")
        [print(builder) for builder in builders]
        sys.exit(0)

    record = report.fetch_records_by_ids([tid])

    path = record[tid]["testroot"]

    if testpath:
        path = record[tid]["testpath"]

    if outfile:
        path = record[tid]["outfile"]

    if errfile:
        path = record[tid]["errfile"]

    if buildscript:
        path = record[tid]["build_script"]

    if stagedir:
        path = record[tid]["stagedir"]

    print(path)
