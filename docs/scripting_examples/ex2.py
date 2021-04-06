import os
from buildtest.defaults import BUILDTEST_ROOT, DEFAULT_SETTINGS_FILE
from buildtest.cli.build import BuildTest

input_buildspecs = [os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml")]


# this will invoke buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml
cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, buildspecs=input_buildspecs)
cmd.discover_buildspecs(printTable=True)
cmd.parse_buildspecs(printTable=True)
cmd.build_phase(printTable=True)
