import logging
import os
import stat

from buildtest.tools.defaults import logID, BUILDTEST_BUILD_HISTORY
from buildtest.tools.buildsystem.status import get_total_build_ids


def write_test(content):
    """Method responsible for writing test script."""

    logger = logging.getLogger(logID)

    build_id = get_total_build_ids()

    logger.info(f"Opening Test File for Writing: {content['testpath']}")

    # This test path doesn't have a build_x folder, is this correct?
    testpath = os.path.expandvars(content['testpath'])
    testdir = os.path.dirname(testpath)

    # Create test directory if doesn't exist
    if not os.path.exists(testdir):
        os.mkdir(testdir)

    with open(testpath, "w") as fd:

        for key, val in content.items():
            # skip key testpath, this key is responsible for opening the file for writing purpose.
            # any value that is empty skip to next key.
            if key == "testpath":
                continue
            if val is None:
                continue
            fd.write("\n".join(val))
            fd.write("\n")

    os.chmod(
        testpath,
        stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
    )

    BUILDTEST_BUILD_HISTORY[build_id]["TESTS"].append(content["testpath"])
