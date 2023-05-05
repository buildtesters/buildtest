import os
import random
import string
import tempfile

import pytest
from buildtest.cli.inspect import (
    inspect_buildspec,
    inspect_by_name,
    inspect_list,
    inspect_query,
)
from buildtest.cli.report import Report
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()

buildtest_report = Report(configuration=configuration)


def test_buildtest_inspect_list():
    # buildtest inspect list
    inspect_list(report=buildtest_report)

    # buildtest inspect list --pager
    inspect_list(report=buildtest_report, pager=True)

    # buildtest inspect list --row-count
    inspect_list(report=buildtest_report, row_count=True)

    # buildtest inspect list --terse --no-header
    inspect_list(report=buildtest_report, terse=True, no_header=True)

    # buildtest inspect list --terse --pager
    inspect_list(report=buildtest_report, terse=True, pager=True)

    # buildtest inspect list --builder
    inspect_list(report=buildtest_report, builder=True)

    # buildtest inspect list --builder --pager
    inspect_list(report=buildtest_report, builder=True, pager=True)


def test_buildtest_inspect_name():
    # select a random test name
    test_names = buildtest_report.get_random_tests(num_items=2)

    print(f"Querying test names: {test_names}")
    # buildtest inspect name <name1> <name2> --pager
    inspect_by_name(report=buildtest_report, names=test_names, pager=True)

    random_testnames = [
        "".join(random.choices(string.ascii_letters, k=10)),
        "".join(random.choices(string.ascii_letters, k=10)),
    ]
    print(f"Querying test names: {random_testnames}")
    with pytest.raises(SystemExit):
        inspect_by_name(report=buildtest_report, names=random_testnames)

    inspect_by_name(
        report=buildtest_report, names=[buildtest_report.builder_names()[0]]
    )


def test_buildspec_inspect_buildspec():
    tf = tempfile.NamedTemporaryFile(delete=True)

    class args:
        subcommands = "inspect"
        inspect = "buildspec"
        buildspec = [tf.name]
        report = None
        all = None
        pager = False

    # if buildspec not in cache we raise error
    with pytest.raises(SystemExit):
        inspect_buildspec(report=buildtest_report, input_buildspecs=[tf.name])

    # delete file
    tf.close()
    # invalid filepath will raise an error
    with pytest.raises(SystemExit):
        inspect_buildspec(report=buildtest_report, input_buildspecs=[tf.name])

    search_buildspec = [
        os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml"),
        os.path.join(BUILDTEST_ROOT, "tutorials", "test_status", "pass_returncode.yml"),
    ]

    # buildtest inspect buildspec $BUILDTEST_ROOT/tutorials/vars.yml $BUILDTEST_ROOT/tutorials/pass_returncode.yml --pager --all
    inspect_buildspec(
        report=buildtest_report,
        input_buildspecs=search_buildspec,
        pager=True,
        all_records=True,
    )


def test_buildtest_query():
    names = buildtest_report.get_names()

    # buildtest inspect query --output --error --testpath --buildscript --buildenv --pager --theme=emacs <name1> <name2> ...
    inspect_query(
        report=buildtest_report,
        name=names,
        output=True,
        error=True,
        testpath=True,
        buildscript=True,
        buildenv=True,
        theme="emacs",
        pager=True,
    )

    # buildtest inspect query stream_test. This test will add coverage where metrics are printed in output
    inspect_query(report=buildtest_report, name=["stream_test"])

    # specifying an invalid test name will raise an exception
    with pytest.raises(SystemExit):
        inspect_query(
            report=buildtest_report,
            name=["".join(random.choices(string.ascii_letters, k=10))],
        )
