from buildtest.cli.show import buildtest_show


def test_buildtest_show():
    buildtest_show(command="build")
    buildtest_show(command="buildspec")
    buildtest_show(command="config")
    buildtest_show(command="cdash")
    buildtest_show(command="path")
    buildtest_show(command="history")
    buildtest_show(command="inspect")
    buildtest_show(command="report")
    buildtest_show(command="schema")
    buildtest_show(command="stylecheck")
    buildtest_show(command="unittests")
