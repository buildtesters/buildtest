import json
import os
import sys
from tabulate import tabulate
from buildtest.defaults import BUILD_HISTORY_DIR
from buildtest.utils.file import walk_tree, load_json, is_dir


def build_history(args):
    """This is the entry point for command ``buildtest build history`` command which reports"""

    if args.history == "list":
        list_builds()

    if args.history == "query":
        query_builds(build_id=args.id, log_option=args.log)


def list_builds():

    history_files = walk_tree(BUILD_HISTORY_DIR, ".json")
    # only filter filters that are 'build.json'
    history_files = [f for f in history_files if os.path.basename(f) == "build.json"]

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

    print(tabulate(table, headers=table.keys(), tablefmt="grid"))


def query_builds(build_id, log_option):
    """This method is called when user runs `buildtest history query` which will
    report the build.json and logfile.

    :param build_id: Input argument `buildtest history query <id>`
    :type build_id: int, required
    :param log_option: Input argument `buildtest history query <id> --log`
    :type log_option: bool, required
    """

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
