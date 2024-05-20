import logging
import os
import re
import sys

from rich.pretty import pprint

from buildtest.defaults import BUILD_HISTORY_DIR, console
from buildtest.utils.file import is_dir, load_json, read_file, walk_tree
from buildtest.utils.table import create_table, print_table, print_terse_format
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

    history_files = sorted_alphanumeric(history_files)
    tdata = process_history_data(history_files)
    headers = [
        "id",
        "user",
        "hostname",
        "system",
        "date",
        "command",
        "pass tests",
        "fail tests",
        "total tests",
        "pass rate",
        "fail rate",
    ]
    table = create_table(
        data=tdata,
        columns=headers,
        title="Build History",
        header_style="blue",
        column_style=consoleColor,
        show_lines=True,
    )

    if terse:
        print_terse_format(
            tdata=tdata,
            headers=headers,
            display_header=no_header,
            color=consoleColor,
            pager=pager,
        )
        return

    print_table(table, pager=pager, row_count=row_count)


def process_history_data(history_files):

    tdata = []
    for fname in history_files:
        row = []
        content = load_json(fname)

        row.append(os.path.basename(os.path.dirname(fname)))

        for field in ["user", "hostname", "system", "date", "command"]:
            row.append(content[field])

        row.append(str(content["test_summary"]["pass"]))
        row.append(str(content["test_summary"]["fail"]))
        row.append(str(content["test_summary"]["total"]))
        row.append(str(content["test_summary"]["pass_rate"]))
        row.append(str(content["test_summary"]["fail_rate"]))

        tdata.append(row)

    return tdata
