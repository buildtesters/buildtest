import os
import random
import string
import tempfile
import uuid

import pytest
from buildtest.cli.inspect import inspect_cmd
from buildtest.cli.report import Report
from buildtest.defaults import BUILDTEST_ROOT


def test_buildtest_inspect_list():

    # running buildtest inspect list --terse
    class args:
        subcommands = "config"
        inspect = "list"
        report = False
        terse = True
        no_header = True

    inspect_cmd(args)

    # running buildtest inspect list --terse
    class args:
        subcommands = "config"
        inspect = "list"
        report = False
        terse = True
        no_header = False

    inspect_cmd(args)

    # running buildtest inspect list
    class args:
        subcommands = "config"
        inspect = "list"
        report = False
        terse = False
        no_header = False

    inspect_cmd(args)


def test_buildtest_inspect_name():

    report = Report()

    # get first two names of list
    test_names = report.get_names()[0]
    # print(test_ids)

    class args:
        subcommands = "config"
        inspect = "name"
        name = [test_names]
        report = None
        all = False

    print(f"Querying test names: {args.name}")
    inspect_cmd(args)

    class args:
        subcommands = "config"
        inspect = "name"
        name = [test_names]
        report = None
        all = True

    print(f"Querying test names: {args.name}")
    inspect_cmd(args)

    class args:
        subcommands = "config"
        inspect = "name"
        name = ["".join(random.choice(string.ascii_letters) for i in range(10))]
        report = None
        all = False

    print(f"Querying test names: {args.name}")
    with pytest.raises(SystemExit):
        inspect_cmd(args)


def test_buildtest_inspect_id():
    report = Report()

    test_ids = report.get_testids()
    identifier = test_ids[0]

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


def test_buildspec_inspect_buildspec():

    tf = tempfile.NamedTemporaryFile(delete=True)

    class args:
        subcommands = "config"
        inspect = "buildspec"
        buildspec = [tf.name]
        report = None
        all = None

    # if buildspec not in cache we raise error
    with pytest.raises(SystemExit):
        inspect_cmd(args)

    # delete file
    tf.close()
    # invalid filepath will raise an error
    with pytest.raises(SystemExit):
        inspect_cmd(args)

    search_buildspec = [
        os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml"),
        os.path.join(BUILDTEST_ROOT, "tutorials", "pass_returncode.yml"),
    ]

    class args:
        subcommands = "config"
        inspect = "buildspec"
        buildspec = search_buildspec
        report = None
        all = False

    # run buildtest inspect buildspec $BUILDTEST_ROOT/tutorials/vars.yml $BUILDTEST_ROOT/tutorials/pass_returncode.yml
    inspect_cmd(args)

    class args:
        subcommands = "config"
        inspect = "buildspec"
        buildspec = search_buildspec
        report = None
        all = True

    # run buildtest inspect buildspec --all $BUILDTEST_ROOT/tutorials/vars.yml $BUILDTEST_ROOT/tutorials/pass_returncode.yml
    inspect_cmd(args)


def test_buildtest_query():

    report = Report()
    names = report.get_names()

    class args:
        subcommands = "config"
        inspect = "query"
        name = names
        report = None
        output = True
        error = True
        testpath = True
        buildscript = True
        display = "last"

    # check buildtest inspect query --output --error --testpath --buildscript -d last <name1> <name2> ...
    inspect_cmd(args)

    class args:
        subcommands = "config"
        inspect = "query"
        name = [names[0]]
        report = None
        output = True
        error = False
        testpath = False
        buildscript = False
        display = "all"

    # check buildtest inspect query --output -d all <name>
    inspect_cmd(args)

    class args:
        subcommands = "config"
        inspect = "query"
        name = [names[0]]
        report = None
        output = True
        error = False
        testpath = False
        buildscript = False
        display = "first"

    # check buildtest inspect query --output -d first <name>
    inspect_cmd(args)

    class args:
        subcommands = "config"
        inspect = "query"
        name = ["".join(random.choice(string.ascii_letters) for i in range(10))]
        report = None
        output = True
        error = False
        testpath = False
        buildscript = False
        display = "first"

    # check invalid test name when querying result which will result in exception SystemExit
    with pytest.raises(SystemExit):
        inspect_cmd(args)
