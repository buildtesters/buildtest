import sys

from buildtest.cli.report import Report


def path_cmd(
    name,
    testpath=None,
    outfile=None,
    errfile=None,
    buildscript=None,
    stagedir=None,
    buildenv=None,
):
    """This is the entry point for ``buildtest path`` command which will display path
    variables for a given test name. If no options are specified we retrieve the root
    directory where test is installed for the latest run for test. One can specify
    a specific test ID by specifying backslash **/** folowed by test identifier.

    Shown below are some examples

    .. code-block::

        # get test root for latest run of 'circle_area'
        bash-3.2$ buildtest path circle_area
        /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.python/python-shell/circle_area/ac3d8bd8

        # get test root for identifier that starts with 'e37'
        bash-3.2$ buildtest path circle_area/e37
        /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.python/python-shell/circle_area/e371dcb8

        # get output file for test circle_area
        bash-3.2$ buildtest path -o circle_area
        /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.python/python-shell/circle_area/ac3d8bd8/circle_area.out

        # get error file for test circle_area
        bash-3.2$ buildtest path -e circle_area
        /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.python/python-shell/circle_area/ac3d8bd8/circle_area.err

    Args:
        name (str): Name of test to search in report file
        testpath (bool): Retrieve path to testpath for a given test
        outfile (bool): Retrieve path output file for a given test
        errfile (bool): Retrieve path to error file for a given test
        buildscript (bool): Retrieve path to build script for a given test
        stagedir (bool): Retrieve path to stage directory for a given test
        buildenv (bool): Retrieve path to buildenv for a given test
    """
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
        for builder in builders:
            print(builder)
        sys.exit(1)

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

    if buildenv:
        path = record[tid]["buildenv"]

    print(path)
