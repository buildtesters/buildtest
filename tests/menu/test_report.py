import os
import pytest
from buildtest.defaults import BUILD_REPORT
from buildtest.menu.report import func_report



def test_func_report_when_BUILD_REPORT_missing():

    try:
        os.remove(BUILD_REPORT)
    except OSError:
        pass

    with pytest.raises(SystemExit):
        func_report()

