import os
import pytest
from shutil import copy
from buildtest.defaults import BUILD_REPORT
from buildtest.menu.report import func_report


def test_report_format():
    class args:
        helpformat = False
        format = None

    func_report(args)

    class args:
        helpformat = False
        format = "name,state,returncode,buildspec"

    func_report(args)

    class args:
        helpformat = False
        format = "badfield,state,returncode"

    with pytest.raises(SystemExit):
        func_report(args)

def test_report_helpformat():
    class args:
        helpformat = True
        format = None

    func_report(args)

def test_func_report_when_BUILD_REPORT_missing():

    backupfile = f"{BUILD_REPORT}.bak"

    try:
        copy(BUILD_REPORT, backupfile)
        os.remove(BUILD_REPORT)
    except OSError:
        pass

    with pytest.raises(SystemExit):
        func_report()
    try:
        move(backupfile, BUILD_REPORT)
    except:
        pass

    assert BUILD_REPORT


