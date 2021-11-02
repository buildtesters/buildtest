import os

from buildtest.cli.build import BuildTest
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT, DEFAULT_SETTINGS_FILE
from buildtest.system import BuildTestSystem

input_buildspecs = [
    os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml"),
    os.path.join(BUILDTEST_ROOT, "general_tests", "configuration"),
]
exclude_buildspecs = [
    os.path.join(BUILDTEST_ROOT, "general_tests", "configuration", "ulimits.yml")
]

buildtest_system = BuildTestSystem()

configuration = SiteConfiguration(DEFAULT_SETTINGS_FILE)
configuration.detect_system()
configuration.validate()

# this will invoke buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml -b $BUILDTEST_ROOT/general_tests/configuration -x $BUILDTEST_ROOT/general_tests/configuration/ulimits.yml --stage=parse
cmd = BuildTest(
    configuration=configuration,
    buildspecs=input_buildspecs,
    exclude_buildspecs=exclude_buildspecs,
    stage="parse",
    buildtest_system=buildtest_system,
)
cmd.build()

discovered_buildspecs = cmd.discovered_buildspecs()

print("Included Buildspecs:", discovered_buildspecs["included"])
print("Excluded Buildspecs:", discovered_buildspecs["excluded"])
print("Detected Buildspecs:", discovered_buildspecs["detected"])
