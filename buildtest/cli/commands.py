def commands_cmd():
    """This method implements command ``buildtest commands`` which shows a list
    of buildtest commands"""

    cmds_list = ["build", "buildspec", "config", "report", "inspect",
                 "path", "history", "schemacdash", "unittests",
                 "stylecheck", "cd", "clean", "docs", "schemadocs",
                 "debugreport", "stats" "info", "help",
                 "tutorial-examples"]

    for x in cmds_list:
        print(x, "\n")
