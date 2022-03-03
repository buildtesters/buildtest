from buildtest.cli.help import buildtest_help


def test_buildtest_help():
    buildtest_help(command="build")
    buildtest_help(command="buildspec")
    buildtest_help(command="config")
    buildtest_help(command="cdash")
    buildtest_help(command="history")
    buildtest_help(command="inspect")
    buildtest_help(command="report")
    buildtest_help(command="schema")
    buildtest_help(command="stylecheck")
    buildtest_help(command="unittests")
