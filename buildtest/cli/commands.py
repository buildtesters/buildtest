from buildtest.cli import BuildTestParser


def list_buildtest_commands():
    """This method implements command ``buildtest commands`` which shows a list of buildtest commands"""

    cmds = BuildTestParser()
    subparser = cmds.get_subparsers()
    buildtest_cmds = sorted(list(subparser.choices.keys()))
    for field in buildtest_cmds:
        print(field)
