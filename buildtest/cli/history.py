import logging
import os
import re
import sys

from rich.pretty import pprint
from rich.table import Table

from buildtest.defaults import BUILD_HISTORY_DIR, console
from buildtest.utils.file import is_dir, load_json, read_file, walk_tree
from buildtest.utils.tools import checkColor

logger = logging.getLogger(__name__)


def build_history(args):
    """This is the entry point for command ``buildtest history`` command which reports

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
    """

    if args.history == "list":
        list_build_history(
            no_header=args.no_header,
            terse=args.terse,
            pager=args.pager,
            color=args.color,
            row_count=args.row_count,
        )

    if args.history == "query":
        query_builds(
            build_id=args.id, log_option=args.log, output=args.output, pager=args.pager
        )


def sorted_alphanumeric(data):
    """This method is used for alphanumeric sorting of files.

    Args:
        data: A list of history files to sort alpha numerically

    Returns:
        list: sorted list of history files alphanumerically
    """

    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(data, key=alphanum_key)


def print_terse(table, no_header=None, consoleColor=None):
    """This method prints the buildtest history list in terse mode which is run via command ``buildtest history list --terse``

    Args:
        table (dict): Table with columns required for the ``buildtest history list`` command.
        no_header (bool, optional): Control whether header columns are displayed with terse format
        consoleColor (bool, optional): Select desired color when displaying results
    """

    row_entry = [table[key] for key in table.keys()]
    transpose_list = [list(i) for i in zip(*row_entry)]
    header = "|".join(table.keys())

    # We print the table columns if --no-header is not specified
    if not no_header:
        console.print(header, style=consoleColor)

    for row in transpose_list:
        line = "|".join(row)
        console.print(f"[{consoleColor}]{line}")


def query_builds(build_id, log_option=None, output=None, pager=None):
    """This method is called when user runs `buildtest history query` which will
    report the build.json and logfile.

    Args:
        build_id (int): Build Identifier which is used for querying history file. The indentifier is an integer starting from 0
        log_option (bool, optional): Option to control whether log file is opened in editor. This is specified via ``buildtest history query -l <id>``
        output (bool, optional): Display output.txt file which contains output of ``buildtest build`` command. This is passed via ``buildtest history query -o``
        pager (bool, optional): Print output in paging format
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

    if output:
        output_content = read_file(
            os.path.join(BUILD_HISTORY_DIR, str(build_id), "output.txt")
        )
        print(output_content)
        return

    if pager:
        with console.pager():
            console.print(content)
        return

    pprint(content)


def create_history_table(table, consoleColor):
    history_table = Table(
        header_style="blue", show_lines=True, row_styles=[consoleColor]
    )
    for field in [
        "id",
        "hostname",
        "user",
        "system",
        "date",
        "pass tests",
        "fail tests",
        "total tests",
        "command",
    ]:
        history_table.add_column(field, overflow="fold")
    for (
        build_id,
        hostname,
        user,
        system,
        date,
        pass_test,
        fail_tests,
        total_tests,
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
        table["command"],
    ):
        history_table.add_row(
            build_id,
            hostname,
            user,
            system,
            date,
            pass_test,
            fail_tests,
            total_tests,
            command,
        )
    return history_table


def list_build_history(
    no_header=None, terse=None, pager=None, color=None, row_count=None
):
    """This method is entry point for ``buildtest history list`` which prints all previous builds
    stored in **BUILD_HISTORY_DIR**. Each directory has a ``build.json`` file that stores content
    of each build that was run by ``buildtest build``.

    Args:
        no_header (bool, optional): Control whether header columns are displayed with terse format
        terse (bool, optional): Print output in terse format
        pager (bool, optional): Print output in paging format
        color (bool, optional): Select desired color when displaying results
        row_count (bool, optional): Print row count of all previous builds
    """
    consoleColor = checkColor(color)
    history_files = walk_tree(BUILD_HISTORY_DIR, ".json")
    # only filter filters that are 'build.json'
    history_files = [f for f in history_files if os.path.basename(f) == "build.json"]
    # There are many ways to calcuate number of history files. There should be one build.json file per subdirectory so a count on number of build.json
    # equal to number of subdirectories in BUILD_HISTORY_DIR
    if row_count:
        print(len(history_files))
        return
    history_files = sorted_alphanumeric(history_files)
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
        if pager:
            with console.pager():
                print_terse(table, no_header, consoleColor)
            return
        print_terse(table, no_header, consoleColor)
        return
    history_table = create_history_table(table, consoleColor)
    if pager:
        with console.pager():
            console.print(history_table)
        return
    console.print(history_table)
