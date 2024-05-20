import logging
import os
import shutil
from functools import reduce

from rich.color import Color, ColorParseError

from buildtest.exceptions import BuildTestError
from buildtest.utils.file import is_dir, resolve_path

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
