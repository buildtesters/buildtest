import os
import shutil

import pytest
from buildtest.cli.build import BuildTest, Tee
from buildtest.cli.history import BUILD_HISTORY_DIR, list_build_history, query_builds
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT, VAR_DIR
from buildtest.system import BuildTestSystem
from rich.color import Color


def test_build_history_list():
    # Testing command:  buildtest history list
    list_build_history(terse=False, no_header=False, pager=False)

    # test with a color: buildtest history list --color <color>
    list_build_history(
        terse=False, no_header=False, pager=False, color=Color.default().name
    )

    # buildtest history list --pager
    list_build_history(terse=False, no_header=False, pager=True)

    # test with terse mode and with color: buildtest --color <Color> history list --terse
    list_build_history(
        terse=True, no_header=False, pager=False, color=Color.default().name
    )

    # test with terse and no header: buildtest history list --terse --no-header
    list_build_history(terse=True, no_header=True, pager=False)


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

    # buildtest history query <id>
    query_builds(build_id=build_id, log_option=False, output=False)

    # buildtest history --pager query <id>
    query_builds(build_id=build_id, log_option=False, output=False, pager=True)

    # buildtest history query <id> --output
    query_builds(build_id=build_id, log_option=False, output=True)

    # buildtest history --pager query <id> --output
    query_builds(build_id=build_id, log_option=False, output=True, pager=True)

    # buildtest history query <id> --log
    query_builds(build_id=build_id, log_option=True, output=False)


def test_invalid_buildid():
    with pytest.raises(SystemExit):
        query_builds(build_id=-1, log_option=True, output=False)

    shutil.rmtree(BUILD_HISTORY_DIR)
    with pytest.raises(SystemExit):
        query_builds(build_id=0, log_option=False, output=False)
