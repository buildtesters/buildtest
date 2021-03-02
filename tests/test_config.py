import os
import pytest
from buildtest.config import check_settings
from buildtest.defaults import DEFAULT_SETTINGS_FILE
from buildtest.executors.setup import BuildExecutor


def test_check_settings():
    settings = check_settings(
        settings_path=DEFAULT_SETTINGS_FILE,
        executor_check=False,
        retrieve_settings=True,
    )
    print(settings)
    assert isinstance(settings, dict)
    # check required keys provided for all system name in configuration file
    for key in ["executors", "moduletool", "load_default_buildspecs", "hostnames"]:
        assert key in settings.keys()


def test_cori_configuration(tmp_path):

    if os.getenv("NERSC_HOST") != "cori":
        pytest.skip("Test runs only on Cori")

    here = os.path.dirname(os.path.abspath(__file__))
    cori_configuration = os.path.join(here, "settings", "cori.config.yml")
    settings = check_settings(cori_configuration, retrieve_settings=True)
    assert isinstance(settings, dict)

    be = BuildExecutor(settings)
    assert be.list_executors() == [
        "local.bash",
        "local.sh",
        "local.csh",
        "local.python",
        "slurm.haswell_debug",
    ]
