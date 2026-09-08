import os

import pytest

from buildtest.cli.build import BuildTest
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem
from buildtest.utils.file import is_file

if os.getenv("BUILDTEST_SLURM_REGRESSION") != "1":
    pytest.skip(
        "Slurm regression tests require BUILDTEST_SLURM_REGRESSION=1",
        allow_module_level=True,
    )


@pytest.mark.slurm
def test_slurm_regression():
    buildtest_root = os.environ["BUILDTEST_ROOT"]
    config_file = os.environ["BUILDTEST_CONFIGFILE"]
    buildspec = os.path.join(buildtest_root, "tests", "examples", "slurm", "ci.yml")

    system = BuildTestSystem()
    configuration = SiteConfiguration(config_file)
    configuration.detect_system()
    configuration.validate(moduletool=system.system["moduletool"])

    build = BuildTest(
        configuration=configuration,
        buildspecs=[buildspec],
        buildtest_system=system,
        poll_interval=1,
    )
    build.build()

    assert len(build.finished_builders) == 3
    for builder in build.finished_builders:
        assert is_file(builder.metadata["outfile"]), builder.metadata["outfile"]
        assert is_file(builder.metadata["errfile"]), builder.metadata["errfile"]
