from buildtest.cli import BuildTestParser


def list_buildtest_commands(with_aliases=None):
    """This method implements command ``buildtest commands`` which shows a list of buildtest commands

    Args:
        with_aliases (bool): Return a list of buildtest commands with aliases
    """

    cmds = BuildTestParser()
    subcmds = sorted(cmds.get_subcommands())

    # if --with-aliases we will show all available choices for subcommands including aliases
    if with_aliases:
        subparser = cmds.get_subparsers()
        subcmds = sorted(list(subparser.choices.keys()))

    for field in sorted(subcmds):
        print(field)
