import logging
import os
import shutil
from functools import reduce

from rich.color import Color, ColorParseError
from rich.syntax import Syntax

from buildtest.defaults import console
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import is_dir, read_file, resolve_path

logger = logging.getLogger(__name__)


def deep_get(dictionary, *keys):
    return reduce(
        lambda d, key: d.get(key, None) if isinstance(d, dict) else None,
        keys,
        dictionary,
    )


def checkColor(colorArg):
    """Checks the provided colorArg against the compatible colors from Rich.Color"""
    if not colorArg:
        return Color.default().name

    if isinstance(colorArg, Color):
        return colorArg.name

    if colorArg and isinstance(colorArg, list):
        colorArg = colorArg[0]
        return colorArg
    if isinstance(colorArg, str):
        try:
            checkedColor = Color.parse(colorArg).name
        except ColorParseError:
            checkedColor = Color.default().name
        return checkedColor


def check_binaries(binaries, custom_dirs=None):
    """Check if binaries exist in $PATH and any additional directories specified by custom_dirs. The return is a dictionary
    containing the binary name and full path to binary.

    Args:
        binaries (list): list of binaries to check for existence in $PATH
        custom_dirs (list, optional): list of custom directories to check for binaries. Defaults to None.

    Returns:
        dict: dictionary containing binary name and full path to binary
    """

    logger.debug(f"Check the following binaries {binaries} for existence.")

    paths = os.getenv("PATH").split(os.pathsep)

    if custom_dirs:
        resolved_path = resolve_path(custom_dirs)
        if is_dir(resolved_path):
            paths.append(resolved_path)

            logger.debug(
                f"Adding directories {resolved_path} to PATH to check for binaries"
            )

    # convert list back to str with colon separated list of directory paths
    paths = ":".join(paths)
    logger.debug(f"Checking PATH directories: {paths}")

    sched_dict = {}
    for command in binaries:
        command_fpath = shutil.which(command, path=paths)
        if not command_fpath:
            logger.error(f"Cannot find {command} command")

        sched_dict[command] = command_fpath
        logger.debug(f"{command}: {command_fpath}")

    return sched_dict


def check_container_runtime(platform, configuration):
    """Check if container runtime exists in $PATH and any additional directories specified by
    custom_dirs. The return is a dictionary

    Args:
        platform (str): platform to check for container runtime
        configuration (dict): configuration dictionary
    """

    binary_path = check_binaries(
        [platform], custom_dirs=deep_get(configuration.target_config, "paths", platform)
    )

    if not binary_path[platform]:
        raise BuildTestError(
            f"[red]Unable to find {platform} binary in PATH, this test will be not be executed.[/red]"
        )

    return binary_path[platform]


def print_file_content(file_path, title, lexer, theme, show_last_lines=None):
    """This method will print the content of a file using Rich Syntax.
    Args:
        file_path (str): Specify file to print the content of.
        title (str): The title to use when printing the content.
        lexer (str): The lexer to use when printing the content.
        theme (str): The theme to use when printing the content.
        show_last_lines (int): Show last N lines of file content. If set to None, will print entire file content.
    """

    content = read_file(file_path)
    console.rule(title)

    trimmed_content = None

    if show_last_lines:
        trimmed_content = content.split("\n")[-show_last_lines:]
        trimmed_content = "\n".join(trimmed_content)

    # if trimmed content is set, we will print a reduced content output otherwise will print entire file
    content = trimmed_content or content

    syntax = Syntax(content, lexer, theme=theme)
    console.print(syntax)
    console.rule()


def print_content(content, title, lexer, theme, show_last_lines=None):
    """This method will print the content using Rich Syntax.

    Args:
        content (str): Specify file to print the content of.
        title (str): The title to use when printing the content.
        lexer (str): The lexer to use when printing the content.
        theme (str): The theme to use when printing the content.
        show_last_lines (int): Show last N lines of file content. If set to None, will print entire file content.
    """

    console.rule(title)

    trimmed_content = None

    if show_last_lines:
        trimmed_content = content.split("\n")[-show_last_lines:]
        trimmed_content = "\n".join(trimmed_content)

    # if trimmed content is set, we will print a reduced content output otherwise will print entire file
    content = trimmed_content or content

    syntax = Syntax(content, lexer, theme=theme)
    console.print(syntax)
    console.rule()
