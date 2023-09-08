from buildtest.cli import BuildTestParser


def list_buildtest_commands():
    """This method implements command ``buildtest commands`` which shows a list of buildtest commands"""

    cmds = BuildTestParser()
    #subparser = cmds.buildtest_subcommands
    #buildtest_cmds = sorted(cmds.buildtest_subcommands)
    for field in sorted(cmds.buildtest_subcommands):
        print(field)
