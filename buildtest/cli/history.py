import os
from tabulate import tabulate
from buildtest.defaults import BUILD_HISTORY_DIR
from buildtest.utils.file import walk_tree, load_json


def build_history():
    """This is the entry point for command ``buildtest build history`` command which reports"""

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
