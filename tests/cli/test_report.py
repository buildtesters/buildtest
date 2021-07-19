import os
import random
import shutil
import string
import tempfile

import pytest
from buildtest.cli.report import Report, report_cmd
from buildtest.defaults import BUILD_REPORT, BUILDTEST_REPORT_SUMMARY, BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError


@pytest.mark.cli
def test_report():

    assert os.path.exists(BUILD_REPORT)

    result = Report()
    print("Processing Report File:", result.reportfile())

    result.print_report()

    # run 'buildtest report --format name,state,returncode,buildspec --terse'
    result.print_report(terse=True)

    # run 'buildtest report --format name,state,returncode,buildspec'
    result = Report(format_args="name,state,returncode,buildspec")
    result.print_report()


@pytest.mark.cli
def test_report_format():

    # buildtest report --helpformat
    report = Report()
    report.print_format_fields()

    # BUILDTEST_COLOR=False buildtest report --helpformat
    os.environ["BUILDTEST_COLOR"] = "False"
    report.print_format_fields()

    # buildtest report --format XYZ is invalid format field
    with pytest.raises(BuildTestError):
        Report(format_args="XYZ")


@pytest.mark.cli
def test_report_filter():

    # run 'buildtest report --helpfilter'
    report = Report()
    report.print_filter_fields()

    # run 'BUILDTEST_COLOR=False buildtest report --helpfilter'
    os.environ["BUILDTEST_COLOR"] = "False"
    report.print_format_fields()

    os.environ["BUILDTEST_COLOR"] = "True"
    report = Report(filter_args={"state": "PASS"})
    report.print_report()

    report = Report(filter_args={"state": "PASS"}, format_args="name,state")
    report.print_report()

    # run 'buildtest report --filter returncode=0,executor=generic.local.bash --format name,returncode,executor
    report = Report(
        filter_args={"returncode": "0", "executor": "generic.local.bash"},
        format_args="name,returncode,executor",
    )
    report.print_report()

    # run 'buildtest report --filter buildspec=tutorials/pass_returncode.yml --format name,returncode,buildspec
    Report(
        filter_args={
            "buildspec": os.path.join(
                BUILDTEST_ROOT, "tutorials", "pass_returncode.yml"
            )
        },
        format_args="name,returncode,buildspec",
    )

    # run 'buildtest report --filter name=exit1_pass --format name,returncode,state
    Report(filter_args={"name": "exit1_pass"}, format_args="name,returncode,state")

    # run 'buildtest report --filter returncode=-999 to ensure _filter_test_by_returncode returns True
    Report(filter_args={"returncode": "-999"})

    # Testing multiple filter fields. 'buildtest report --filter tags=tutorials,executor=generic.local.bash,state=PASS,returncode=0 --format name,returncode,state,executor,tags
    Report(
        filter_args={
            "tags": "tutorials",
            "executor": "generic.local.bash",
            "state": "PASS",
            "returncode": 0,
        },
        format_args="name,returncode,state,executor,tags",
    )


@pytest.mark.cli
def test_report_oldest_and_latest():

    # buildtest report --filter tags=tutorials --latest
    Report(filter_args={"tags": "tutorials"}, latest=True)

    # buildtest report --filter tags=tutorials --oldest
    Report(filter_args={"tags": "tutorials"}, oldest=True)

    # buildtest report --filter tags=tutorials --oldest --latest
    Report(filter_args={"tags": "tutorials"}, oldest=True, latest=True)


@pytest.mark.cli
def test_invalid_filters():

    # run 'buildtest report --filter state=UNKNOWN --format name,state',
    # this raises error because UNKNOWN is not valid value for state field
    with pytest.raises(SystemExit):
        Report(filter_args={"state": "UNKNOWN"}, format_args="name,state")

    tf = tempfile.NamedTemporaryFile(delete=True)
    tf.close()
    # test invalid buildspec file that doesn't exist in filesystem
    with pytest.raises(SystemExit):
        Report(filter_args={"buildspec": tf.name}, format_args="name,returncode,state")

    # run 'buildtest report --filter buildspec=$HOME/.bashrc --format name,returncode,state
    # this will raise error even though file is valid it won't be found in cache
    with pytest.raises(SystemExit):
        Report(
            filter_args={"buildspec": "$HOME/.bashrc"},
            format_args="name,returncode,state",
        )

    # buildtest report --filter returncode=1.5 is invalid returncode (must be INT)
    with pytest.raises(BuildTestError):
        Report(filter_args={"returncode": "1.5"})

    # buildtest report --filter XYZ=tutorials is invalid filter field
    with pytest.raises(BuildTestError):
        Report(filter_args={"XYZ": "tutorials"})


@pytest.mark.cli
def test_invalid_report_files():

    tf = tempfile.NamedTemporaryFile(delete=True)

    # reading a report file not in JSON format will result in exception BuildTestError
    with pytest.raises(BuildTestError):
        Report(report_file=tf.name)

    # closing the file will delete the file from file-system
    tf.close()
    # An invalid path for report file will raise an exception
    with pytest.raises(SystemExit):
        Report(report_file=tf.name)

    tempdir = tempfile.TemporaryDirectory()
    with pytest.raises(SystemExit):
        Report(report_file=tempdir.name)


@pytest.mark.cli
def test_report_list():
    class args:
        helpformat = False
        helpfilter = False
        filter = None
        format = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = "list"
        terse = None

    report_cmd(args)

    # now removing report summary it should print a message
    os.remove(BUILDTEST_REPORT_SUMMARY)
    report_cmd(args)


@pytest.mark.cli
def test_report_clear():
    class args:
        helpformat = False
        helpfilter = False
        filter = None
        format = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None
        terse = None

    backupfile = BUILD_REPORT + ".bak"
    shutil.copy2(BUILD_REPORT, backupfile)
    report_cmd(args)
    shutil.move(backupfile, BUILD_REPORT)
    assert BUILD_REPORT

    class args:
        helpformat = False
        helpfilter = False
        filter = None
        format = None
        oldest = False
        latest = False
        report = "".join(random.choice(string.ascii_letters) for i in range(10))
        report_subcommand = "clear"
        terse = None

    # buildtest report clear <file> will raise an error since file doesn't exist
    with pytest.raises(SystemExit):
        report_cmd(args)
