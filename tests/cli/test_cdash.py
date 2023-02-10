import os

import pytest
import requests
from buildtest.cli.build import BuildTest
from buildtest.cli.cdash import upload_test_cdash, view_cdash_project
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.system import BuildTestSystem
from buildtest.utils.tools import deep_get

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


@pytest.mark.cli
def test_cdash_view():
    cdash_config = deep_get(configuration.target_config, "cdash")
    view_cdash_project(
        cdash_config=cdash_config, config_file=configuration.file, open_browser=False
    )


@pytest.mark.cli
def test_cdash_upload():
    system = BuildTestSystem()
    cmd = BuildTest(
        buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "shell_examples.yml")],
        buildtest_system=system,
        configuration=configuration,
    )
    cmd.build()

    upload_test_cdash(
        build_name="TESTING",
        configuration=configuration,
        site="GENERIC",
        open_browser=False,
    )


def test_cdash_upload_exceptions():
    # a buildname must be specified, a None will result in error
    with pytest.raises(SystemExit):
        upload_test_cdash(
            build_name=None,
            configuration=configuration,
            site="GENERIC",
            open_browser=False,
        )

    here = os.path.dirname(__file__)

    bc = SiteConfiguration(
        os.path.abspath(os.path.join(here, "cdash_examples", "invalid_url.yml"))
    )
    bc.detect_system()

    # in configuration file we have invalid url to CDASH server
    with pytest.raises(requests.ConnectionError):
        upload_test_cdash(
            build_name="DEMO",
            configuration=bc,
        )

    bc = SiteConfiguration(
        os.path.abspath(os.path.join(here, "cdash_examples", "invalid_project.yml"))
    )
    bc.detect_system()

    # in configuration file we have invalid project name in CDASH

    with pytest.raises(SystemExit):
        upload_test_cdash(
            build_name="DEMO", configuration=bc, site=None, open_browser=False
        )
