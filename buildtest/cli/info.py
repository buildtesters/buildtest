import os
import shutil

from rich.panel import Panel

from buildtest import BUILDTEST_VERSION
from buildtest.defaults import (
    BUILD_HISTORY_DIR,
    BUILD_REPORT,
    BUILDSPEC_CACHE_FILE,
    console,
)
from buildtest.executors.setup import BuildExecutor
from buildtest.tools.cpu import cpuinfo
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import is_dir, is_file


def buildtest_info(configuration, buildtest_system):
    """Entry point for ``buildtest info`` command which will print some basic information pertaining to buildtest and system details captured
        during system detection.

    Args:
        configuration (buildtest.config.SiteConfiguration, optional): Loaded configuration content which is an instance of SiteConfiguration
        buildtest_system (buildtest.system.BuildTestSystem, optional): Instance of BuildTestSystem class
    """

    be = BuildExecutor(configuration)
    cpu_details = cpuinfo()

    buildtest_details = [
        f"[red]Buildtest Version:[/red]        [green]{BUILDTEST_VERSION}[/green]",
        f"[red]Buildtest Path:[/red]           [green]{shutil.which('buildtest')}[/green]",
        f"[red]Configuration File:[/red]       [green]{configuration.file}[/green]",
        f"[red]Available Systems:[/red]        [green]{configuration.systems}[/green]",
        f"[red]Active System:[/red]            [green]{configuration.name()}[/green]",
        f"[red]Available Executors:[/red]      [green]{be.names()}[/green]",
    ]
    system_details = [
        f"[red]Python Path:[/red]               [green]{buildtest_system.system['python']}[/green]",
        f"[red]Python Version:[/red]            [green]{buildtest_system.system['pyver']}[/green]",
        f"[red]Host:[/red]                      [green]{buildtest_system.system['host']}[/green]",
        f"[red]Operating System:[/red]          [green]{buildtest_system.system['os']}[/green]",
        f"[red]Module System:[/red]             [green]{buildtest_system.system['moduletool']}[/green]",
        f"[red]Architecture:[/red]              [green]{cpu_details['arch']}[/green]",
        f"[red]Vendor:[/red]                    [green]{cpu_details['vendor']}[/green]",
        f"[red]Model:[/red]                     [green]{cpu_details['model']}[/green]",
        f"[red]Platform:[/red]                  [green]{cpu_details['platform']}[/green]",
        f"[red]CPU:[/red]                       [green]{cpu_details['cpu']}[/green]",
        f"[red]Virtual CPU:[/red]               [green]{cpu_details['vcpu']}[/green]",
        f"[red]Sockets:[/red]                   [green]{cpu_details['num_sockets']}[/green]",
        f"[red]Cores per Socket:[/red]          [green]{cpu_details['num_cpus_per_socket']}[/green]",
        f"[red]Virtual Memory Total:[/red]      [green]{cpu_details['virtualmemory']['total']} MB[/green]",
        f"[red]Virtual Memory Used:[/red]       [green]{cpu_details['virtualmemory']['used']} MB[/green]",
        f"[red]Virtual Memory Available:[/red]  [green]{cpu_details['virtualmemory']['available']} MB[/green]",
        f"[red]Virtual Memory Free:[/red]       [green]{cpu_details['virtualmemory']['free']} MB[/green]",
    ]

    if is_dir(BUILD_HISTORY_DIR):
        buildtest_details.extend(
            [
                f"[red]Build History Directory:[/red]  [green]{BUILD_HISTORY_DIR}[/green]",
                f"[red]Number of builds:[/red]         [green]{len(os.listdir(BUILD_HISTORY_DIR))}[/green]",
            ]
        )

    if is_file(BUILDSPEC_CACHE_FILE):
        buildtest_details.append(
            f"[red]Buildspec Cache File:[/red]     [green]{BUILDSPEC_CACHE_FILE}[/green]"
        )
    else:
        buildtest_details.append("[red]Buildspec Cache File does not exist")

    if is_file(BUILD_REPORT):
        buildtest_details.append(
            f"[red]Default Report File:[/red]      [green]{BUILD_REPORT}[/green]"
        )
    else:
        buildtest_details.append("[red]Default report file does not exist")

    console.print(
        Panel.fit("\n".join(buildtest_details), title="buildtest details"),
        justify="left",
    )
    console.print(
        Panel.fit("\n".join(system_details), title="system details"), justify="left"
    )

    for package in ["black", "pyflakes", "isort"]:
        print_version_info(package)


def print_version_info(command_name):
    """Print version information for any command by running --version

    Args:
        command_name (str): Name of command to run with --version
    """
    cmd = BuildTestCommand(f"{command_name} --version")
    cmd.execute()

    console.print(f"{command_name}: {shutil.which(command_name)}")
    console.print(f"{command_name} version: {''.join(cmd.get_output())}")
