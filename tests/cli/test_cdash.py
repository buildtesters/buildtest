import os
import pytest
from buildtest.cli.cdash import cdash_cmd
from buildtest.config import SiteConfiguration
from buildtest.defaults import DEFAULT_SETTINGS_FILE


def test_cdash_view():

    configuration = SiteConfiguration()
    configuration.get_current_system()
    configuration.validate()

    class args:
        cdash = "view"
        url = None
        config = None

    cdash_cmd(args=args, default_configuration=configuration, open_browser=False)

    class args:
        cdash = "view"
        config = DEFAULT_SETTINGS_FILE
        url = None

    cdash_cmd(args, open_browser=False)


def test_cdash_upload():
    class args:
        cdash = "upload"
        config = DEFAULT_SETTINGS_FILE
        buildname = "TESTING"
        site = None
        report_file = None

    cdash_cmd(args)


def test_cdash_upload_exceptions():
    class args:
        cdash = "upload"
        config = DEFAULT_SETTINGS_FILE
        buildname = None
        site = None
        report_file = None

    # a buildname must be specified, a None will result in error
    with pytest.raises(SystemExit):
        cdash_cmd(args)

    here = os.path.dirname(__file__)

    class args:
        cdash = "upload"
        config = os.path.abspath(
            os.path.join(here, "cdash_examples", "invalid_url.yml")
        )
        buildname = "DEMO"
        site = None
        report_file = None

    # in configuration file we have invalid url to CDASH server
    with pytest.raises(SystemExit):
        cdash_cmd(args)

    class args:
        cdash = "upload"
        config = os.path.abspath(
            os.path.join(here, "cdash_examples", "invalid_project.yml")
        )
        buildname = "DEMO"
        site = None
        report_file = None

    # in configuration file we have invalid project name in CDASH
    with pytest.raises(SystemExit):
        cdash_cmd(args)
