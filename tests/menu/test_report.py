import os
import pytest
import shutil
from buildtest.defaults import BUILD_REPORT
from buildtest.menu.report import func_report


def test_func_report():

    backup_report = f"{BUILD_REPORT}.bak"
    assert BUILD_REPORT

    try:
        shutil.copyfile(BUILD_REPORT, backup_report)
        os.remove(BUILD_REPORT)
    except OSError:
        pass
    # when BUILD_REPORT file not found, func_report will raise error
    with pytest.raises(SystemExit):
        func_report()

    try:
        shutil.move(backup_report, BUILD_REPORT)
    except OSError:
        pass

    func_report()
