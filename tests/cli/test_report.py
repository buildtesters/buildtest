import datetime
import os
import shutil
import tempfile

import pytest
from rich.color import Color

from buildtest.cli.report import (
    Report,
    clear_report,
    list_report,
    report_cmd,
    report_summary,
)
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILD_REPORT, BUILDTEST_REPORTS, BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import is_file

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


@pytest.mark.cli
def test_report():
    # assert os.path.exists(BUILD_REPORT)

    result = Report(configuration)
    print("Processing Report File:", result.reportfile())

    result.print_report()

    # run 'buildtest --color <Color> report --format name,state,returncode,buildspec --terse'
    result.print_report(terse=True, color=Color.default().name)

    result.print_report(row_count=True)

    # run 'buildtest report --format name,state,returncode,buildspec'
    result = Report(
        configuration=configuration, format_args="name,state,returncode,buildspec"
    )
    result.print_report()

    result = Report(configuration, pager=True)
    result.print_report()
    result = Report(configuration, color="red")
    result.print_report()
    result = Report(configuration, color="red", pager=True)
    result.print_report()
    result = Report(configuration, color="BAD_COLOR")
    result.print_report()
    result = Report(configuration, color="BAD_COLOR", pager=True)
    result.print_report()


@pytest.mark.cli
def test_report_format():
    # buildtest report --helpformat
    report = Report(configuration)
    report.print_format_fields()

    # buildtest report --formatfields
    report.print_raw_format_fields()

    # buildtest report --format XYZ is invalid format field
    with pytest.raises(BuildTestError):
        Report(configuration, format_args="XYZ")


@pytest.mark.cli
def test_report_filter():
    # run 'buildtest report --helpfilter'
    report = Report(configuration)
    report.print_filter_fields()

    # run 'buildtest report --filterfields'
    report.print_raw_filter_fields()

    # run 'buildtest report --helpfilter'
    report.print_format_fields()

    report = Report(configuration, filter_args={"state": "PASS"})
    report.print_report()

    report = Report(
        configuration, filter_args={"state": "PASS"}, format_args="name,state"
    )
    report.print_report()

    # run 'buildtest report --filter returncode=0,executor=generic.local.bash --format name,returncode,executor
    report = Report(
        configuration=configuration,
        filter_args={"returncode": "0", "executor": "generic.local.bash"},
        format_args="name,returncode,executor",
    )
    report.print_report()

    # run 'buildtest report --filter buildspec=tutorials/pass_returncode.yml --format name,returncode,buildspec
    Report(
        configuration=configuration,
        filter_args={
            "buildspec": os.path.join(
                BUILDTEST_ROOT, "tutorials", "test_status", "pass_returncode.yml"
            )
        },
        format_args="name,returncode,buildspec",
    )

    # run 'buildtest report --filter name=exit1_pass --format name,returncode,state
    Report(
        configuration=configuration,
        filter_args={"name": "exit1_pass"},
        format_args="name,returncode,state",
    )

    # run 'buildtest report --filter returncode=-999 to ensure _filter_test_by_returncode returns True
    Report(configuration=configuration, filter_args={"returncode": "-999"})

    # Testing multiple filter fields. 'buildtest report --filter tags=tutorials,executor=generic.local.bash,state=PASS,returncode=0 --format name,returncode,state,executor,tags
    Report(
        configuration=configuration,
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
    Report(configuration=configuration, filter_args={"tags": "tutorials"}, latest=True)

    # buildtest report --filter tags=tutorials --oldest
    Report(configuration=configuration, filter_args={"tags": "tutorials"}, oldest=True)

    # buildtest report --filter tags=tutorials --oldest --latest
    Report(
        configuration=configuration,
        filter_args={"tags": "tutorials"},
        oldest=True,
        latest=True,
    )


@pytest.mark.cli
def test_report_failure():
    # buildtest report --filter tags=tutorials --fail
    Report(configuration=configuration, filter_args={"tags": "tutorials"}, failure=True)


@pytest.mark.cli
def test_report_passed():
    # buildtest report --filter tags=tutorials --pass
    Report(configuration=configuration, filter_args={"tags": "tutorials"}, passed=True)


@pytest.mark.cli
def test_report_start_and_end():
    start_date = datetime.datetime.strptime("2022-06-07 00:00:00", "%Y-%m-%d %X")
    end_date = datetime.datetime.now()

    # buildtest report --filter tags=tutorials --start
    Report(
        configuration=configuration, filter_args={"tags": "tutorials"}, start=start_date
    )

    # buildtest report --filter tags=tutorials --end
    Report(configuration=configuration, filter_args={"tags": "tutorials"}, end=end_date)

    # buildtest report --filter tags=tutorials --start --end
    Report(
        configuration=configuration,
        filter_args={"tags": "tutorials"},
        start=start_date,
        end=end_date,
    )


@pytest.mark.cli
def test_invalid_filters():
    # run 'buildtest report --filter state=UNKNOWN --format name,state',
    # this raises error because UNKNOWN is not valid value for state field
    with pytest.raises(BuildTestError):
        Report(
            configuration=configuration,
            filter_args={"state": "UNKNOWN"},
            format_args="name,state",
        )

    tf = tempfile.NamedTemporaryFile(delete=True)
    tf.close()
    # test invalid buildspec file that doesn't exist in filesystem
    with pytest.raises(BuildTestError):
        Report(
            configuration=configuration,
            filter_args={"buildspec": tf.name},
            format_args="name,returncode,state",
        )

    # run 'buildtest report --filter buildspec=$HOME/.bashrc --format name,returncode,state
    # this will raise error even though file is valid it won't be found in cache
    with pytest.raises(BuildTestError):
        Report(
            configuration=configuration,
            filter_args={"buildspec": "$HOME/.bashrc"},
            format_args="name,returncode,state",
        )

    # buildtest report --filter returncode=1.5 is invalid returncode (must be INT)
    with pytest.raises(BuildTestError):
        Report(configuration=configuration, filter_args={"returncode": "1.5"})

    # buildtest report --filter XYZ=tutorials is invalid filter field
    with pytest.raises(BuildTestError):
        Report(configuration=configuration, filter_args={"XYZ": "tutorials"})


@pytest.mark.cli
def test_invalid_report_files():
    tf = tempfile.NamedTemporaryFile(delete=True)

    # reading a report file not in JSON format will result in exception BuildTestError
    with pytest.raises(BuildTestError):
        Report(configuration=configuration, report_file=tf.name)

    # closing the file will delete the file from file-system
    tf.close()
    # An invalid path for report file will raise an exception
    with pytest.raises(SystemExit):
        Report(configuration=configuration, report_file=tf.name)

    tempdir = tempfile.TemporaryDirectory()
    with pytest.raises(SystemExit):
        Report(configuration=configuration, report_file=tempdir.name)


@pytest.mark.cli
def test_report_summary():
    report = Report(configuration=configuration)
    report_summary(report, configuration=configuration)

    # buildtest rt summary --pager
    report = Report(configuration=configuration, pager=True)
    report_summary(report, configuration=configuration)

    # buildtest rt summary --detailed
    report = Report(configuration=configuration)
    report_summary(report, configuration=configuration, detailed=True)

    # buildtest rt summary --detailed --pager
    report = Report(configuration=configuration, pager=True)
    report_summary(report, configuration=configuration, detailed=True)

    report = Report(configuration=configuration, color="light_pink1")
    report_summary(report, configuration=configuration)

    report = Report(configuration=configuration, pager=True, color="light_pink1")
    report_summary(report, configuration=configuration, detailed=True)

    # buildtest --color light_pink1 rt sm --detailed
    report = Report(configuration=configuration, color="light_pink1")
    report_summary(report, configuration=configuration, detailed=True)

    # buildtest rt sm --detailed --pager
    report = Report(configuration=configuration, pager=True)
    report_summary(report, configuration=configuration, detailed=True)

    # buildtest --color BAD_COLOR rt sm --detailed
    report = Report(configuration=configuration, color="BAD_COLOR")
    report_summary(report, configuration=configuration, detailed=True)


@pytest.mark.cli
def test_report_list():
    list_report()
    backupfile = tempfile.NamedTemporaryFile()
    shutil.copy2(BUILDTEST_REPORTS, backupfile.name)

    # now removing report summary it should print a message
    os.remove(BUILDTEST_REPORTS)

    with pytest.raises(SystemExit):
        list_report()

    # move back the removed BUILDTEST_REPORTS file
    shutil.move(backupfile.name, BUILDTEST_REPORTS)
    assert is_file(BUILDTEST_REPORTS)


@pytest.mark.cli
def test_report_clear():
    backupfile_report = tempfile.NamedTemporaryFile()
    shutil.copy2(BUILD_REPORT, backupfile_report.name)

    backupfile_list_report = tempfile.NamedTemporaryFile()
    shutil.copy2(BUILDTEST_REPORTS, backupfile_list_report.name)

    clear_report()

    # buildtest report clear will raise an error since file doesn't exist
    with pytest.raises(SystemExit):
        clear_report()

    assert not is_file(BUILD_REPORT)
    # move back the backe-up files since report_cmd() function removes the files BUILD_REPORT and BUILDTEST_REPORTS
    shutil.move(backupfile_report.name, BUILD_REPORT)

    shutil.move(backupfile_list_report.name, BUILDTEST_REPORTS)

    assert is_file(BUILD_REPORT)
    assert is_file(BUILDTEST_REPORTS)


@pytest.mark.cli
def test_report_limited_rows():
    report = Report(configuration=configuration)
    report.print_report(count=5)
    report.print_report(terse=True, count=5)
    # test report query with 0 and negative number with and without terse mode
    report.print_report(terse=False, count=0)
    report.print_report(terse=False, count=-1)
    report.print_report(terse=True, count=0)
    report.print_report(terse=True, count=-1)


@pytest.mark.cli
def test_report_path():
    class args:
        filter = None
        format = None
        start = None
        end = None
        fail = None
        passed = None
        oldest = False
        latest = False
        report_subcommand = "path"
        count = None
        color = None
        pager = None

    report_cmd(args, configuration=configuration)
