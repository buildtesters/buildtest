import os
import random
import shutil
import string
import tempfile

import pytest

from buildtest.defaults import BUILD_REPORT, BUILDTEST_ROOT, BUILDTEST_REPORT_SUMMARY
from buildtest.cli.report import report_cmd
from buildtest.exceptions import BuildTestError


@pytest.mark.cli
def test_report_format():

    assert os.path.exists(BUILD_REPORT)

    class args:
        helpformat = False
        helpfilter = False
        format = None
        filter = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report'
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        format = "name,state,returncode,buildspec"
        filter = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --format name,state,returncode,buildspec'
    report_cmd(args)


@pytest.mark.cli
def test_invalid_format():
    class args:
        helpformat = False
        helpfilter = False
        filter = None
        format = "XYZ"
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # buildtest report --format XYZ is invalid format field
    with pytest.raises(BuildTestError):
        report_cmd(args)


@pytest.mark.cli
def test_report_helpformat():
    class args:
        helpformat = True
        helpfilter = False
        format = None
        filter = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    report_cmd(args)


@pytest.mark.cli
def test_report_filter():
    class args:
        helpformat = False
        helpfilter = True
        format = None
        filter = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --helpfilter'
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"state": "PASS"}
        format = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --filter state=PASS'
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"state": "PASS"}
        format = "name,state"
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --filter state=PASS --format name,state'
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"state": "UNKNOWN"}
        format = "name,state"
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --filter state=UNKNOWN --format name,state',
    # this raises error because UNKNOWN is not valid value for state field
    with pytest.raises(SystemExit):
        report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"returncode": "0", "executor": "local.bash"}
        format = "name,returncode,executor"
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --filter returncode=0,executor=local.bash --format name,returncode,executor
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {
            "buildspec": os.path.join(
                BUILDTEST_ROOT, "tutorials", "pass_returncode.yml"
            )
        }
        format = "name,returncode,buildspec"
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --filter buildspec=tutorials/pass_returncode.yml --format name,returncode,buildspec
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"name": "exit1_pass"}
        format = "name,returncode,state"
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --filter name=exit1_pass --format name,returncode,state
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"returncode": "-999"}
        format = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --filter returncode=-999 to ensure _filter_test_by_returncode returns True
    report_cmd(args)

@pytest.mark.cli
def test_report_oldest_and_latest():
    class args:
        helpformat = False
        helpfilter = False
        filter = {"tags": "tutorials"}
        format = None
        oldest = False
        latest = True
        report = BUILD_REPORT
        report_subcommand = None

    # buildtest report --filter tags=tutorials --latest
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"tags": "tutorials"}
        format = None
        oldest = True
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # buildtest report --filter tags=tutorials --oldest
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"tags": "tutorials"}
        format = None
        oldest = True
        latest = True
        report = BUILD_REPORT
        report_subcommand = None

    # buildtest report --filter tags=tutorials --oldest --latest
    report_cmd(args)

@pytest.mark.cli
def test_invalid_filters():
    class args:
        helpformat = False
        helpfilter = False
        filter = {
            "buildspec": "".join(random.choice(string.ascii_letters) for i in range(10))
        }
        format = "name,returncode,state"
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # the filter argument buildspec is a random string which will be invalid file
    # and we expect an exception to be raised
    with pytest.raises(SystemExit):
        report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"buildspec": "$HOME/.bashrc"}
        format = "name,returncode,state"
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --filter buildspec=$HOME/.bashrc --format name,returncode,state
    # this will raise error even though file is valid it won't be found in cache
    with pytest.raises(SystemExit):
        report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {
            "tags": "tutorials",
            "executor": "local.bash",
            "state": "PASS",
            "returncode": 0,
        }
        format = "name,returncode,state,executor,tags"
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # run 'buildtest report --filter tags=tutorials,executor=local.bash,state=PASS,returncode=0 --format name,returncode,state,executor,tags
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {
            "returncode": "1.5",
        }
        format = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # buildtest report --filter returncode=1.5 is invalid returncode (must be INT)
    with pytest.raises(BuildTestError):

        report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {
            "XYZ": "tutorials",
        }
        format = None
        oldest = False
        latest = False
        report = BUILD_REPORT
        report_subcommand = None

    # buildtest report --filter XYZ=tutorials is invalid filter field
    with pytest.raises(BuildTestError):
        report_cmd(args)

@pytest.mark.cli
def test_invalid_report_format():

    tf = tempfile.NamedTemporaryFile()

    class args:
        helpformat = False
        helpfilter = False
        filter = None
        format = None
        oldest = False
        latest = False
        report = tf.name
        report_subcommand = None

    # reading a report file not in JSON format will result in exception BuildTestError
    with pytest.raises(BuildTestError):
        report_cmd(args)

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

    # buildtest report clear <file> will raise an error since file doesn't exist
    with pytest.raises(SystemExit):
        report_cmd(args)


def test_report_missing_file():
    class args:
        helpformat = False
        helpfilter = False
        filter = None
        format = None
        oldest = False
        latest = False
        report = "".join(random.choice(string.ascii_letters) for i in range(10))
        report_subcommand = None

    with pytest.raises(SystemExit):
        report_cmd(args)
