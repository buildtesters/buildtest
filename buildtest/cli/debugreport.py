import os

from rich.syntax import Syntax

from buildtest.cli import BUILDTEST_VERSION
from buildtest.cli.config import view_configuration
from buildtest.defaults import console


def print_debug_report(system, configuration):
    """This method will print debug report for buildtest. This will print system information,
    configuration and last buildtest log file"""

    """
    console.print("Vendor: ", system.system["vendor"])
    console.print("Machine: ", system.system["machine"])
    console.print("MicroArchitecture Name: ", system.system["arch"])
    console.print("Model: ", system.system["model"])
    """

    console.print("Host:", system.system["host"])
    console.print("OS:", system.system["os"])
    console.print("Python: ", system.system["python"])
    console.print("Python Version: ", system.system["pyver"])
    console.print("BUILDTEST_VERSION: ", BUILDTEST_VERSION)
    console.print("Machine: ", system.system["machine"])

    view_configuration(configuration)

    last_log = os.path.join(os.getenv("BUILDTEST_ROOT"), "var", "buildtest.log")
    if os.path.exists(last_log):
        console.rule(last_log)
        with open(last_log, "r") as bc:
            syntax = Syntax(bc.read(), "log", line_numbers=True, theme="emacs")
        console.print(syntax)
