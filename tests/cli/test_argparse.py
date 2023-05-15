import argparse

import pytest
from buildtest.cli import (
    build_filters_format,
    get_parser,
    handle_kv_string,
    positive_number,
    supported_color,
    valid_time,
)


def test_positive_number():
    assert 1 == positive_number(1)
    with pytest.raises(argparse.ArgumentTypeError) as err:
        positive_number(0)
        print(err)

    # input argument must be integer or string
    with pytest.raises(argparse.ArgumentTypeError):
        positive_number([1, 2, 3])

    with pytest.raises(ValueError):
        positive_number("hello")


def test_handle_kv_string():
    assert {"tags": "fail"} == handle_kv_string("tags=fail")

    assert {"tags": "fail", "type": "script"} == handle_kv_string(
        "tags=fail,type=script"
    )

    # missing equal sign with multiple keys
    with pytest.raises(argparse.ArgumentTypeError) as err:
        handle_kv_string("tags,type,script")
        print(err)

    # missing equal sign with single key
    with pytest.raises(argparse.ArgumentTypeError):
        handle_kv_string("tags")


def test_buildtest_build_filters():
    assert {
        "tags": ["fail", "pass"],
        "type": ["script"],
        "maintainers": ["shahzebsiddiqui"],
    } == build_filters_format("tags=fail,pass;type=script;maintainers=shahzebsiddiqui")
    build_filters_format("tags=fail")

    # missing equal sign with multiple keys
    with pytest.raises(argparse.ArgumentTypeError) as err:
        build_filters_format("tags=fail,pass;type;maintainers=shahzebsiddiqui")
        print(err)

    # missing equal sign with single key
    with pytest.raises(argparse.ArgumentTypeError) as err:
        build_filters_format("tags")
        print(err)


def test_supported_colors():
    rich_color = supported_color("red")
    assert rich_color.name == "red"

    # input must be a string
    with pytest.raises(argparse.ArgumentTypeError):
        supported_color(["red"])

    assert supported_color("xyz") is None


def test_valid_time():
    valid_time("2022-01-01")
    # input must be a string not a list
    with pytest.raises(argparse.ArgumentTypeError):
        valid_time(["2022-01-01"])

    # raises exception when its unable to convert time
    with pytest.raises(ValueError):
        valid_time("2022-01-01 abcdef")


def test_arg_parse():
    parser = get_parser()
    print(parser)

    assert parser.prog == "buildtest"
    assert parser.usage == "%(prog)s [options] [COMMANDS]"
