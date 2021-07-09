import random
import string
import uuid

import pytest

from buildtest.cli.inspect import get_all_ids, inspect_cmd
from buildtest.defaults import BUILD_REPORT
from buildtest.utils.file import load_json


def test_buildtest_inspect_list():
    class args:
        subcommands = "config"
        inspect = "list"
        report = False

    inspect_cmd(args)


def test_buildtest_inspect_name():

    report = load_json(BUILD_REPORT)
    test_ids = get_all_ids(report)
    # print(test_ids)

    # get first element's value from dict. dict in format  { <ID> : <name>, <ID>: <name> }
    test_name = list(test_ids.values())[0]

    class args:
        subcommands = "config"
        inspect = "name"
        name = [test_name]
        report = None

    print(f"Querying test names: {args.name}")
    print(args)
    inspect_cmd(args)

    class args:
        subcommands = "config"
        inspect = "name"
        name = ["".join(random.choice(string.ascii_letters) for i in range(10))]
        report = None

    print(f"Querying test names: {args.name}")
    with pytest.raises(SystemExit):
        inspect_cmd(args)


def test_buildtest_inspect_id():
    report = load_json(BUILD_REPORT)
    test_ids = get_all_ids(report)

    identifier = list(test_ids.keys())[0]

    class args:
        subcommands = "config"
        inspect = "id"
        id = [identifier]
        report = None

    print(f"Querying test identifier: {args.id}")
    inspect_cmd(args)

    class args:
        subcommands = "config"
        inspect = "id"
        id = [str(uuid.uuid4())]
        report = None

    print(f"Querying test identifier: {args.id}")
    # generate a random unique id which is not a valid test id when searching for tests by id.
    with pytest.raises(SystemExit):
        inspect_cmd(args)
