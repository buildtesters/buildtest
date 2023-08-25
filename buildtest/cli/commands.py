def list_buildtest_commands():
    """This method implements command ``buildtest commands`` which shows a list of buildtest commands"""

    cmds_list = [
        "build",
        "buildspec",
        "cd",
        "cdash",
        "clean",
        "config",
        "debugreport",
        "docs",
        "history",
        "info",
        "inspect",
        "path",
        "report",
        "schema",
        "schemadocs",
        "show",
        "stats",
        "stylecheck",
        "tutorial-examples",
        "unittests",
    ]

    for field in cmds_list:
        print(field)
