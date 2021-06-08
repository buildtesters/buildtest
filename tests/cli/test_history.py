import pytest
from buildtest.cli.history import query_builds, build_history


def test_build_history():
    class args:
        history = "list"

    # buildtest build history
    build_history(args)

    class args:
        history = "query"
        id = 0
        log = False

    build_history(args)


def test_invalid_buildid():

    with pytest.raises(SystemExit):
        query_builds(build_id=-1, log_option=True)
