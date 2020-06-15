import json
import sys
from buildtest.defaults import BUILD_REPORT
from buildtest.utils.file import is_file

def func_report(args):

    # raise error if BUILD_REPORT not found
    if not is_file(BUILD_REPORT):
        sys.exit(f"Unable to fetch report no such file found: {BUILD_REPORT}")

    report = None
    with open(BUILD_REPORT, "r") as fd:
        report = json.loads(fd.read())

    # if report is None or issue with how json.load returns content of file we
    # raise error
    if not report:
        sys.exit(f"Fail to process {BUILD_REPORT} please check if file is valid json"
                 f"or remove file")

    print ("{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("name", "state", "returncode","starttime","endtime","runtime", "buildid","buildspec"))

    for buildspec in report.keys():
        for name in report[buildspec].keys():
            for test in report[buildspec][name]:
                print("{:<20} {:<20} {:<20} {:<20} {:<20} {:06.2f} {:<20} {:<20}".format(name, test["state"], test["returncode"], test["starttime"], test["endtime"], test['runtime'], test["build_id"], buildspec))

