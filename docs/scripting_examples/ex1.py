import os
from buildtest.defaults import BUILDTEST_ROOT, DEFAULT_SETTINGS_FILE
from buildtest.menu.build import BuildTest

input_buildspecs = [
    os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml"),
    os.path.join(BUILDTEST_ROOT, "general_tests", "configuration"),
]
exclude_buildspecs = [
    os.path.join(BUILDTEST_ROOT, "general_tests", "configuration", "ulimits.yml")
]

# this will invoke buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml -b $BUILDTEST_ROOT/general_tests/configuration -x $BUILDTEST_ROOT/general_tests/configuration/ulimits.yml --stage=parse
cmd = BuildTest(
    config_file=DEFAULT_SETTINGS_FILE,
    buildspecs=input_buildspecs,
    exclude_buildspecs=exclude_buildspecs,
    stage="parse",
)
cmd.build()


print("\nDiscovered buildspecs: ")
for name in cmd.bp_found:
    print(name)

print("\nRemoved buildspecs: ")
for name in cmd.bp_removed:
    print(name)


print("\nDetected buildspecs:")
for name in cmd.detected_buildspecs:
    print(name)
