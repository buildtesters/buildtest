import pytest
from buildtest.cli.history import build_history, query_builds


def test_build_history():
    class args:
        history = "list"
        terse = False
        no_header = False

    # buildtest build history
    build_history(args)

    class args:
        history = "list"
        terse = True
        no_header = False

    # 'buildtest build history list --terse'
    build_history(args)

    class args:
        history = "list"
        terse = True
        no_header = True

    # 'buildtest build history list --terse --no-header'
    build_history(args)

    class args:
        history = "query"
        id = 0
        log = False

    # 'buildtest build history query 0'
    build_history(args)


def test_invalid_buildid():

    with pytest.raises(SystemExit):
        query_builds(build_id=-1, log_option=True)
