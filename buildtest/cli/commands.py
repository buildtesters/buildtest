from buildtest.defaults import console
from rich.table import Table


def commands_cmd():
    """This method implements command ``buildtest commands`` which shows a list
    of buildtest commands"""

    table = Table(title=None, show_lines=False)
    table.add_column(None, justify="left", style="magenta")

    table.add_row("build")
    table.add_row("buildspec")
    table.add_row("config")
    table.add_row("report")
    table.add_row("inspect")
    table.add_row("path")
    table.add_row("history")
    table.add_row("schema")
    table.add_row("cdash")
    table.add_row("unittests")
    table.add_row("stylecheck")
    table.add_row("cd")
    table.add_row("clean")
    table.add_row("docs")
    table.add_row("schemadocs")
    table.add_row("debugreport")
    table.add_row("stats")
    table.add_row("info")
    table.add_row("help")
    table.add_row("tutorial-examples")

    console.print(table)
