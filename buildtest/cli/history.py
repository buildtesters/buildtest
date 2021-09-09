import json
import logging
import os
import re
import sys

from buildtest.defaults import BUILD_HISTORY_DIR
from buildtest.utils.file import is_dir, load_json, walk_tree
from tabulate import tabulate

logger = logging.getLogger(__name__)


def build_history(args):
    """This is the entry point for command ``buildtest build history`` command which reports

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
    """

    if args.history == "list":
        list_builds(header=args.no_header, terse=args.terse)

    if args.history == "query":
        query_builds(build_id=args.id, log_option=args.log)


def sorted_alphanumeric(data):
    """This method is used for alpha numeric sorting of files.

    Args:
        data: A list of history files to sort alpha numerically

    Returns:
        list: sorted list of history files alphanumerically
    """

    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(data, key=alphanum_key)


def list_builds(header=None, terse=None):
    """This method is entry point for ``buildtest history list`` which prints all previous builds
    stored in **BUILD_HISTORY_DIR**. Each directory has a ``build.json`` file that stores content
    of each build that was run by ``buildtest build``.

    Args:
        header (bool, optional): Control whether header columns are displayed with terse format
        terse (bool, optional): Print output in terse format
    """

    history_files = walk_tree(BUILD_HISTORY_DIR, ".json")
    logger.debug(f"Searching for all '.json' files in directory: {BUILD_HISTORY_DIR}")

    # only filter filters that are 'build.json'
    history_files = [f for f in history_files if os.path.basename(f) == "build.json"]

    # sort all files alpha-numerically
    history_files = sorted_alphanumeric(history_files)

    logger.info(f"We have detected {len(history_files)} history files")
    for file in history_files:
        logger.info(file)

    table = {
        "id": [],
        "hostname": [],
        "user": [],
        "system": [],
        "date": [],
        "pass_tests": [],
        "fail_tests": [],
        "total_tests": [],
        "pass_rate": [],
        "fail_rate": [],
        "command": [],
    }

    for fname in history_files:
        content = load_json(fname)

        table["id"].append(os.path.basename(os.path.dirname(fname)))
        for field in ["user", "hostname", "system", "date", "command"]:
            table[field].append(content[field])

        table["pass_tests"].append(content["test_summary"]["pass"])
        table["fail_tests"].append(content["test_summary"]["fail"])
        table["total_tests"].append(content["test_summary"]["total"])
        table["pass_rate"].append(content["test_summary"]["pass_rate"])
        table["fail_rate"].append(content["test_summary"]["fail_rate"])

    if terse:

        # We print the table columns if --no-header is not specified
        if not header:
            print("|".join(table.keys()))

        for (
            build_id,
            hostname,
            user,
            system,
            date,
            pass_test,
            fail_tests,
            total_tests,
            pass_rate,
            fail_rate,
            command,
        ) in zip(
            table["id"],
            table["hostname"],
            table["user"],
            table["system"],
            table["date"],
            table["pass_tests"],
            table["fail_tests"],
            table["total_tests"],
            table["pass_rate"],
            table["fail_rate"],
            table["command"],
        ):
            print(
                f"{build_id}|{hostname}|{user}|{date}|{pass_test}|{fail_tests}|{total_tests}|{pass_rate}|{fail_rate}|{command}"
            )
        return

    print(tabulate(table, headers=table.keys(), tablefmt="grid"))


def query_builds(build_id, log_option):
    """This method is called when user runs `buildtest history query` which will
    report the build.json and logfile.

    Args:
        build_id (int): Build Identifier which is used for querying history file. The indentifier is an integer starting from 0
        log_option (bool): Option to control whether log file is opened in editor. This is specified via ``buildtest history query -l <id>``
    """

    if not is_dir(BUILD_HISTORY_DIR):
        sys.exit(
            f"Unable to find history directory: {BUILD_HISTORY_DIR}, seems like you have not run any builds using 'buildtest build' command."
        )

    num_ids = list(range(len(os.listdir(BUILD_HISTORY_DIR))))

    if not is_dir(os.path.join(BUILD_HISTORY_DIR, str(build_id))):
        sys.exit(
            f"Invalid build id: {build_id}. Please select one of the following build ids: {num_ids}"
        )

    content = load_json(os.path.join(BUILD_HISTORY_DIR, str(build_id), "build.json"))

    # if --log option specified open file in vim
    if log_option:
        os.system(f"vim {content['logpath']}")
        return

    print(json.dumps(content, indent=2))
