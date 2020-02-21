import logging
import os
import stat

from buildtest.tools.config import logID, BUILDTEST_BUILD_HISTORY
from buildtest.tools.buildsystem.status import get_total_build_ids


def write_test(dict):
    """Method responsible for writing test script."""

    logger = logging.getLogger(logID)

    build_id = get_total_build_ids()

    fd = open(dict["testpath"], "w")
    logger.info(f"Opening Test File for Writing: {dict['testpath']}")

    for key, val in dict.items():
        # skip key testpath, this key is responsible for opening the file for writing purpose.
        # any value that is empty skip to next key.
        if key == "testpath":
            continue
        if val is None:
            continue
        fd.write("\n".join(val))
        fd.write("\n")

    fd.close()

    os.chmod(
        dict["testpath"],
        stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
    )

    BUILDTEST_BUILD_HISTORY[build_id]["TESTS"].append(dict["testpath"])
