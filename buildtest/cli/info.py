import os
import shutil

from buildtest import BUILDTEST_VERSION
from buildtest.defaults import (
    BUILD_HISTORY_DIR,
    BUILD_REPORT,
    BUILDSPEC_CACHE_FILE,
    console,
)
from buildtest.executors.setup import BuildExecutor
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import is_dir, is_file
from rich.panel import Panel


def buildtest_info(configuration, buildtest_system):
    """Entry point for ``buildtest info`` command which will print some basic information pertaining to buildtest and system details captured
        during system detection.

    Args:
        configuration (buildtest.config.SiteConfiguration, optional): Loaded configuration content which is an instance of SiteConfiguration
        buildtest_system (buildtest.system.BuildTestSystem, optional): Instance of BuildTestSystem class
    """

    be = BuildExecutor(configuration)

    buildtest_details = f"""
[red]Buildtest Version:[/red]        [green]{BUILDTEST_VERSION}[/green]
[red]Buildtest Path:[/red]           [green]{shutil.which('buildtest')}[/green]
[red]Configuration File:[/red]       [green]{configuration.file}[/green]
[red]Available Systems:[/red]        [green]{configuration.systems}[/green]
[red]Active System:[/red]            [green]{configuration.name()}[/green]
[red]Available Executors:[/red]      [green]{be.names()}[/green]
"""

    system_details = f"""
[red]Python Path:[/red]         [green]{buildtest_system.system['python']}[/green]
[red]Python Version:[/red]      [green]{buildtest_system.system['pyver']}[/green]
[red]Processor:[/red]           [green]{buildtest_system.system['processor']}[/green]
[red]Host:[/red]                [green]{buildtest_system.system['host']}[/green]
[red]Machine:[/red]             [green]{buildtest_system.system['machine']}[/green]
[red]Operating System:[/red]    [green]{buildtest_system.system['os']}[/green]
[red]Module System:[/red]       [green]{buildtest_system.system['moduletool']}[/green]
"""

    if is_dir(BUILD_HISTORY_DIR):
        buildtest_details += f"[red]Build History Directory:[/red]  [green]{BUILD_HISTORY_DIR}[/green] \n"
        buildtest_details += f"[red]Number of builds:[/red]         [green]{len(os.listdir(BUILD_HISTORY_DIR))}[/green] \n"

        # console.print(f"Build History Directory: {BUILD_HISTORY_DIR}")

        # console.print(f"Number of builds in history: {len(os.listdir(BUILD_HISTORY_DIR))}")

    if is_file(BUILDSPEC_CACHE_FILE):
        buildtest_details += f"[red]Buildspec Cache File:[/red]     [green]{BUILDSPEC_CACHE_FILE}[/green] \n"
        # console.print(f"Buildspec Cache File: {BUILDSPEC_CACHE_FILE}")
    else:
        buildtest_details += "[red]Buildspec Cache File does not exist"

        # console.print(f"Buildspec Cache File does not exist")

    if is_file(BUILD_REPORT):
        buildtest_details += (
            f"[red]Default Report File:[/red]      [green]{BUILD_REPORT}[/green]"
        )
        # console.print(f"Default Report File: {BUILD_REPORT}")
    else:
        buildtest_details += "[red]Default report file does not exist"
        # console.print(f"Default report file does not exist")

    console.print(
        Panel.fit(buildtest_details, title="buildtest details"), justify="left"
    )
    console.print(Panel.fit(system_details, title="system details"), justify="left")

    cmd = BuildTestCommand("black --version")
    cmd.execute()

    console.print(f"black: {shutil.which('black')}")
    console.print(f"black version: {''.join(cmd.get_output())}")

    cmd = BuildTestCommand("pyflakes --version")
    cmd.execute()

    console.print(f"pyflakes: {shutil.which('pyflakes')}")
    console.print(f"pyflakes version: {''.join(cmd.get_output())}")

    cmd = BuildTestCommand("isort --version")
    cmd.execute()

    console.print(f"isort: {shutil.which('isort')}")
    console.print(f"{' '.join(cmd.get_output())}")
