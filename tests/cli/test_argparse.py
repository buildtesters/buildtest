import argparse
import pytest

from buildtest.cli import positive_number, handle_kv_string, get_parser


def test_positive_number():
    assert 1 == positive_number(1)
    with pytest.raises(argparse.ArgumentTypeError) as err:
        positive_number(0)
        print(err)


def test_handle_kv_string():

    assert {"tags": "fail"} == handle_kv_string("tags=fail")

    assert {"tags": "fail", "type": "script"} == handle_kv_string(
        "tags=fail,type=script"
    )

    with pytest.raises(argparse.ArgumentTypeError) as err:
        handle_kv_string("tags,type,script")
        print(err)


def test_arg_parse():

    parser = get_parser()
    print(parser)

    assert parser.prog == "buildtest"
    assert parser.usage == "%(prog)s [options] [COMMANDS]"
