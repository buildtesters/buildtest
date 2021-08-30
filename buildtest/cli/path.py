from buildtest.cli.report import Report
from buildtest.exceptions import BuildTestError


def path_cmd(
    name, testpath=None, outfile=None, errfile=None, buildscript=None, stagedir=None
):
    report = Report()
    names = report.get_names()
    if name not in names:
        raise BuildTestError(f"Please specify one of the following test names: {names}")

    # by default print attribute testroot if no options specified
    path = report.get_path_by_name(name, "testroot")

    if testpath:
        path = report.get_path_by_name(name, "testpath")

    if outfile:
        path = report.get_path_by_name(name, "outfile")

    if errfile:
        path = report.get_path_by_name(name, "errfile")

    if buildscript:
        path = report.get_path_by_name(name, "build_script")

    if stagedir:
        path = report.get_path_by_name(name, "stagedir")

    print(path)
