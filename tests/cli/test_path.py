import random
import string

import pytest
from buildtest.cli.path import path_cmd
from buildtest.cli.report import Report
from buildtest.exceptions import BuildTestError


def test_path():

    report = Report()
    names = report.get_names()
    name = names[0]

    path_cmd(name)

    path_cmd(name, outfile=True)
    path_cmd(name, errfile=True)
    path_cmd(name, stagedir=True)
    path_cmd(name, testpath=True)
    path_cmd(name, buildscript=True)

    random_test_name = "".join(random.choice(string.ascii_letters) for i in range(10))

    with pytest.raises(BuildTestError):
        path_cmd(random_test_name)
