import logging
import os
import shutil
import sys
from jsonschema import validate

from buildtest.buildsystem.schemas.utils import load_schema
from buildtest.defaults import (
    BUILDTEST_SETTINGS_FILE,
    DEFAULT_SETTINGS_FILE,
    DEFAULT_SETTINGS_SCHEMA,
)
from buildtest.system import get_slurm_partitions, get_slurm_qos, get_slurm_clusters
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import create_dir, is_dir, is_file

logger = logging.getLogger(__name__)


def create_settings_file(settings_file):
    """If default settings file don't exist, copy the default settings provided by buildtest."""

    if not is_file(settings_file):
        logger.debug(f"Detected File: {settings_file} is not present")
        shutil.copy(DEFAULT_SETTINGS_FILE, settings_file)
        logger.debug(f"Copying file: {DEFAULT_SETTINGS_FILE} to {settings_file}")


def init(settings_path):
    """Buildtest init should check that the buildtest user root exists,
       and that dependency files are created. This is called by 
       ``load_settings``.
    """

    # if settings_path is not defined dirname is equivalent to BUILDTEST_ROOT, since BUILDTEST_SETTINGS_FILE is in BUILDTEST_ROOT
    dirname = os.path.dirname(settings_path)

    # check if $HOME/.buildtest exists, if not create directory
    if not is_dir(dirname):
        create_dir(dirname)
        msg = f"Creating buildtest settings directory: {dirname}"
        logger.info(msg)

    # Create subfolders site
    create_dir(os.path.join(dirname, "site"))

    # Create settings files
    create_settings_file(settings_path)


def check_settings(settings_path=None, run_init=True, executor_check=True):
    """Checks all keys in configuration file (settings/settings.yml) are valid
       keys and ensure value of each key matches expected type . For some keys
       special logic is taken to ensure values are correct and directory path
       exists.       

       If any error is found buildtest will terminate immediately.

       Parameters:

       :param settings_path: Path to buildtest settings file
       :type settings_path: str, optional

       :return: returns gracefully if all checks passes otherwise terminate immediately
       :rtype: exit code 1 if checks failed
    """

    user_schema = load_settings(settings_path, run_init)

    config_schema = load_schema(DEFAULT_SETTINGS_SCHEMA)
    logger.debug(f"Loading default settings schema: {DEFAULT_SETTINGS_SCHEMA}")

    logger.debug(f"Validating user schema with schema: {DEFAULT_SETTINGS_SCHEMA}")
    validate(instance=user_schema, schema=config_schema)
    logger.debug("Validation was successful")

    # only perform executor check if executor_check is True. This is default
    # behavior, this can be disabled only for regression test where executor check
    # such as slurm check are not applicable.
    if executor_check:
        slurm_executors = user_schema.get("executors", {}).get("slurm")

        if slurm_executors:
            validate_slurm_executors(slurm_executors)


def load_settings(settings_path=None, run_init=True):
    """Load the default settings file if no argument is specified.

       Parameters:

       :param settings_path: Path to buildtest settings file
       :type settings_path: str, optional
    """

    settings_path = settings_path or BUILDTEST_SETTINGS_FILE

    if run_init:
        init(settings_path)

    # load the settings file into a schema object
    return load_schema(settings_path)


def get_default_settings():
    """Load and return the default buildtest settings file. """

    return load_settings()


def validate_slurm_executors(slurm_executor):
    """This method will validate slurm executors, we check if partition, qos,
       and cluster fields are valid values by retrieving details from slurm configuration.
       These checks are performed if ``partition``, ``qos`` or ``cluster`` field
       is specified in slurm executor section.

       :param slurm_executor: list of slurm executors defined in settings['executors]['slurm'] dictionary, where settings is loaded buildtest setting
    """

    slurm_partitions = get_slurm_partitions()
    slurm_qos = get_slurm_qos()
    slurm_cluster = get_slurm_clusters()

    for executor in slurm_executor:

        # if 'partition' key defined check if its valid partition
        if slurm_executor[executor].get("partition"):

            if slurm_executor[executor]["partition"] not in slurm_partitions:
                sys.exit(
                    f"{slurm_executor[executor]['partition']} not a valid partition!. Please select one of the following partitions: {slurm_partitions}"
                )

            query = f"sinfo -p {slurm_executor[executor]['partition']} -h -O available"
            cmd = BuildTestCommand(query)
            cmd.execute()
            part_state = "".join(cmd.get_output())
            part_state = part_state.rstrip()
            # check if partition is in 'up' state. If not we raise an error.
            if part_state != "up":
                sys.exit(
                    f"{slurm_executor[executor]['partition']} is in state: {part_state}. It must be in 'up' state in order to accept jobs"
                )
        # check if 'qos' key is valid qos
        if slurm_executor[executor].get("qos"):

            if slurm_executor[executor]["qos"] not in slurm_qos:
                sys.exit(
                    f"{slurm_executor[executor]['qos']} not a valid qos! Please select one of the following qos: {slurm_qos}"
                )
        # check if 'cluster' key is valid slurm cluster
        if slurm_executor[executor].get("cluster"):

            if slurm_executor[executor]["cluster"] not in slurm_cluster:
                sys.exit(
                    f"{slurm_executor[executor]['cluster']} not a valid slurm cluster! Please select one of the following slurm clusters: {slurm_cluster}"
                )
