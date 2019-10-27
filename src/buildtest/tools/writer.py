import logging
import json
import os
import subprocess
import sys
import stat

from buildtest.tools.config import logID, BUILDTEST_BUILD_HISTORY
from buildtest.tools.buildsystem.status import get_total_build_ids

def write_test(dict,verbose):
    """Method responsible for writing test script."""

    logger = logging.getLogger(logID)

    build_id = get_total_build_ids()

    fd = open(dict["testpath"],"w")
    logger.info(f"Opening Test File for Writing: {dict['testpath']}")

    if verbose >= 2:
        print (f"{json.dump(dict,sys.stdout,indent=4)}")

    for key,val in dict.items():
        # skip key testpath, this key is responsible for opening the file for writing purpose.
        # any value that is emptry skip to next key.
        if key == "testpath" or len(val) == 0:
            continue
        fd.write("\n".join(val))
        fd.write("\n")

    fd.close()
    print (f"Writing Test: {dict['testpath']}")

    os.chmod(dict["testpath"], stat.S_IRWXU |
                               stat.S_IRGRP |
                               stat.S_IXGRP |
                               stat.S_IROTH |
                               stat.S_IXOTH)

    if verbose >= 1:
        print (f"Changing permission to 755 for test: {dict['testpath']}")

    if verbose >= 2:
        test_output = subprocess.getoutput(f"cat {dict['testpath']}").splitlines()
        print ("{:_<80}".format(""))
        for line in test_output:
            print (line)
        print ("{:_<80}".format(""))

    BUILDTEST_BUILD_HISTORY[build_id]["TESTS"] = [dict["testpath"]]
