import os
import shutil

import pytest
from buildtest.cli.build import BuildTest, Tee
from buildtest.cli.history import BUILD_HISTORY_DIR, list_build_history, query_builds
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT, VAR_DIR
from buildtest.system import BuildTestSystem


def test_build_history_list():
    list_build_history(terse=False, header=False, pager=False)
    list_build_history(terse=False, header=False, pager=True)

    list_build_history(terse=True, header=False, pager=False)
    list_build_history(terse=True, header=True, pager=False)


def test_build_history_query():

    fname = os.path.join(VAR_DIR, "output.txt")
    configuration = SiteConfiguration()

    configuration.detect_system()
    configuration.validate()

    system = BuildTestSystem()

    with Tee(fname):
        cmd = BuildTest(
            buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml")],
            buildtest_system=system,
            configuration=configuration,
        )
        cmd.build()

    build_history_dir = cmd.get_build_history_dir()
    shutil.move(fname, os.path.join(build_history_dir, "output.txt"))

    build_id = list(range(len(os.listdir(BUILD_HISTORY_DIR))))[-1]
    print(build_id)

    # run buildtest history query <id>
    query_builds(build_id=build_id, log_option=False, output=False)

    # run buildtest history query <id> --output
    query_builds(build_id=build_id, log_option=False, output=True)

    # run buildtest history query <id> --log
    query_builds(build_id=build_id, log_option=True, output=False)


def test_invalid_buildid():

    with pytest.raises(SystemExit):
        query_builds(build_id=-1, log_option=True, output=False)

    shutil.rmtree(BUILD_HISTORY_DIR)
    with pytest.raises(SystemExit):
        query_builds(build_id=0, log_option=False, output=False)
