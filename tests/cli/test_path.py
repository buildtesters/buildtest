import random
import string

import pytest
from buildtest.cli.path import path_cmd
from buildtest.cli.report import Report
from buildtest.config import SiteConfiguration

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


def test_path():
    report = Report(configuration=configuration)
    names = report.get_names()
    name = names[0]

    path_cmd(name, configuration=configuration)

    path_cmd(name, configuration=configuration, outfile=True)
    path_cmd(name, configuration=configuration, errfile=True)
    path_cmd(name, configuration=configuration, stagedir=True)
    path_cmd(name, configuration=configuration, testpath=True)
    path_cmd(name, configuration=configuration, buildscript=True)
    path_cmd(name, configuration=configuration, buildenv=True)

    builders = report.builder_names()
    # specify name in format 'buildtest path <name>/<testid>
    path_cmd(
        name=builders[0],
        configuration=configuration,
    )

    random_test_name = "".join(random.choices(string.ascii_letters, k=10))

    with pytest.raises(SystemExit):
        path_cmd(
            random_test_name,
            configuration=configuration,
        )
