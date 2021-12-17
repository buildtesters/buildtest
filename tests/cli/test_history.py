import os
import shutil

import pytest
from buildtest.cli.build import BuildTest, Tee
from buildtest.cli.history import BUILD_HISTORY_DIR, build_history, query_builds
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT, VAR_DIR
from buildtest.system import BuildTestSystem


def test_build_history_list():
    class args:
        history = "list"
        terse = False
        no_header = False

    # buildtest build history
    build_history(args)

    class args:
        history = "list"
        terse = True
        no_header = False

    # 'buildtest build history list --terse'
    build_history(args)

    class args:
        history = "list"
        terse = True
        no_header = True

    # 'buildtest build history list --terse --no-header'
    build_history(args)


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

    num_ids = list(range(len(os.listdir(BUILD_HISTORY_DIR))))[-1]
    print(num_ids)

    class args:
        history = "query"
        id = num_ids
        log = False
        output = False

    # 'buildtest build history query <ID>'
    build_history(args)

    class args:
        history = "query"
        id = num_ids
        log = False
        output = True

    # 'buildtest build history query --output <ID>'
    build_history(args)


def test_invalid_buildid():

    with pytest.raises(SystemExit):
        query_builds(build_id=-1, log_option=True, output=False)

    shutil.rmtree(BUILD_HISTORY_DIR)
    with pytest.raises(SystemExit):
        query_builds(build_id=0, log_option=False, output=False)
