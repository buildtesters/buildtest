import os
import pytest
import random
import shutil
import string
from buildtest.defaults import BUILD_REPORT, BUILDTEST_ROOT
from buildtest.cli.report import report_cmd


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

    # run 'buildtest report'
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        format = "name,state,returncode,buildspec"
        filter = None
        oldest = False
        latest = False

    # run 'buildtest report --format name,state,returncode,buildspec'
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        format = "badfield,state,returncode"
        filter = None
        oldest = False
        latest = False

    # specify invalid format field 'badfield'
    with pytest.raises(SystemExit):
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

    # run 'buildtest report --helpfilter'
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"state": "PASS"}
        format = None
        oldest = False
        latest = False

    # run 'buildtest report --filter state=PASS'
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"state": "PASS"}
        format = "name,state"
        oldest = False
        latest = False

    # run 'buildtest report --filter state=PASS --format name,state'
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"state": "UNKNOWN"}
        format = "name,state"
        oldest = False
        latest = False

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

    # run 'buildtest report --filter buildspec=tutorials/pass_returncode.yml --format name,returncode,buildspec
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {"name": "exit1_pass"}
        format = "name,returncode,state"
        oldest = False
        latest = False

    # run 'buildtest report --filter name=exit1_pass --format name,returncode,state
    report_cmd(args)

    class args:
        helpformat = False
        helpfilter = False
        filter = {
            "buildspec": "".join(random.choice(string.ascii_letters) for i in range(10))
        }
        format = "name,returncode,state"
        oldest = False
        latest = False

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

    # run 'buildtest report --filter tags=tutorials,executor=local.bash,state=PASS,returncode=0 --format name,returncode,state,executor,tags
    report_cmd(args)


def test_report_cmd_when_BUILD_REPORT_missing():

    backupfile = f"{BUILD_REPORT}.bak"

    try:
        shutil.copy(BUILD_REPORT, backupfile)
        os.remove(BUILD_REPORT)
    except OSError:
        pass

    class args:
        helpformat = False
        helpfilter = False
        filter = None
        format = None
        oldest = False
        latest = False

    with pytest.raises(SystemExit):
        report_cmd(args)

    shutil.move(backupfile, BUILD_REPORT)

    assert BUILD_REPORT
