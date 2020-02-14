import json
import os
import sys


sys.path.insert(0, os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest"))
# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"

from buildtest.tools.menu import BuildTestParser
from buildtest.tools.system import BuildTestSystem
from buildtest.tools.config import check_configuration, BUILDTEST_MODULE_COLLECTION_FILE, BUILDTEST_BUILD_LOGFILE
from buildtest.tools.file import create_dir


def main():
    """Entry point to buildtest."""

    create_dir(os.path.join(os.getenv("BUILDTEST_ROOT"), "var"))
    if not os.path.exists(BUILDTEST_MODULE_COLLECTION_FILE):
        module_coll_dict = {"collection": []}
        with open(BUILDTEST_MODULE_COLLECTION_FILE, "w") as outfile:
            json.dump(module_coll_dict, outfile, indent=2)

    if not os.path.exists(BUILDTEST_BUILD_LOGFILE):
        build_dict = {"build": {}}
        with open(BUILDTEST_BUILD_LOGFILE, "w") as outfile:
            json.dump(build_dict, outfile, indent=2)

    buildtest_system = BuildTestSystem()
    buildtest_system.check_system_requirements()

    check_configuration()

    parser = BuildTestParser()
    parser.parse_options()

if __name__ == "__main__":
    """Entry Point, invoking main() method"""
    main()
