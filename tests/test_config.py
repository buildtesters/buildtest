import os
import pytest
from jsonschema import ValidationError
from buildtest.config import check_settings
from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.executors.setup import BuildExecutor
from buildtest.exceptions import BuildTestError


def test_check_settings():
    settings = check_settings(executor_check=False, retrieve_settings=True)
    assert isinstance(settings, dict)
    assert "executors" in settings.keys()
    assert "moduletool" in settings.keys()
    assert "load_default_buildspecs" in settings.keys()


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
