import logging
import os
import sys
from jsonschema import validate

from buildtest.schemas.utils import load_schema, load_recipe
from buildtest.defaults import (
    BUILDTEST_SETTINGS_FILE,
    DEFAULT_SETTINGS_FILE,
    DEFAULT_SETTINGS_SCHEMA,
)
from buildtest.system import (
    get_slurm_partitions,
    get_slurm_qos,
    get_slurm_clusters,
    get_lsf_queues,
)
from buildtest.utils.command import BuildTestCommand


logger = logging.getLogger(__name__)


def check_settings(settings_path=None, executor_check=True, retrieve_settings=False):
    """Checks all keys in configuration file (settings/config.yml) are valid
    keys and ensure value of each key matches expected type. For some keys
    special logic is taken to ensure values are correct and directory path
    exists. If any error is found buildtest will terminate immediately.

    :param settings_path: Path to buildtest settings file
    :type settings_path: str, optional
    :param executor_check: boolean to control if executor checks are performed
    :type executor_check: bool
    :param retrieve_settings: return loaded buildtest settings that is validated by schema. By default, this method doesn't return anything other than validating buildtest settings
    :type retrieve_settings: bool
    :return: returns gracefully if all checks passes otherwise terminate immediately
    :rtype: exit code 1 if checks failed
    """

    user_schema = load_settings(settings_path)

    logger.debug(f"Loading default settings schema: {DEFAULT_SETTINGS_SCHEMA}")
    config_schema = load_schema(DEFAULT_SETTINGS_SCHEMA)

    logger.debug(f"Validating user schema with schema: {DEFAULT_SETTINGS_SCHEMA}")
    validate(instance=user_schema, schema=config_schema)
    logger.debug("Validation was successful")

    # only perform executor check if executor_check is True. This is default
    # behavior, this can be disabled only for regression test where executor check
    # such as slurm check are not applicable.
    if executor_check:
        slurm_executors = user_schema.get("executors", {}).get("slurm")
        lsf_executors = user_schema.get("executors", {}).get("lsf")

        if slurm_executors:
            validate_slurm_executors(slurm_executors)

        if lsf_executors:
            validate_lsf_executors(lsf_executors)

    if retrieve_settings:
        return user_schema


def load_settings(settings_path=None):
    """Load the default settings file if no argument is specified.

    :param settings_path: Path to buildtest settings file
    :type settings_path: str, optional
    """

    settings_path = settings_path

    if not settings_path:
        settings_path = resolve_settings_file()

    # load the settings file into a schema object
    return load_recipe(settings_path)


def resolve_settings_file():
    """Returns path to buildtest settings file that should be used. If there
       is a user defined buildtest settings ($HOME/.buildtest/config.yml) it will
       be honored, otherwise default settings from buildtest will be used.
    """
    # if buildtest settings file exist return it otherwise return default file
    if os.path.exists(BUILDTEST_SETTINGS_FILE):
        return BUILDTEST_SETTINGS_FILE

    return DEFAULT_SETTINGS_FILE


def validate_lsf_executors(lsf_executors):
    """This method validates all LSF executors. We check if queue is available
    and in ``Open:Active`` state.
    :param lsf_executors: A list of LSF executors to validate
    :type lsf_executors: dict
    """
    queue_dict = get_lsf_queues()

    queue_list = []
    valid_queue_state = "Open:Active"
    record = queue_dict["RECORDS"]
    # retrieve all queues from json record
    for name in record:
        queue_list.append(name["QUEUE_NAME"])

    # check all executors have defined valid queues and check queue state.
    for executor in lsf_executors:
        queue = lsf_executors[executor].get("queue")
        # if queue field is defined check if its valid queue
        if queue:
            if queue not in queue_list:
                sys.exit(
                    f"{lsf_executors[executor]['queue']} not a valid partition!. Please select one of the following partitions: {queue_list}"
                )

            # check queue record for Status
            for name in record:

                # skip record until we find matching queue
                if name["QUEUE_NAME"] != queue:
                    continue

                queue_state = name["STATUS"]
                # if state not Open:Active we raise error
                if not queue_state == valid_queue_state:
                    sys.exit(
                        f"{lsf_executors[executor]['queue']} is in state: {queue_state}. It must be in {valid_queue_state} state in order to accept jobs"
                    )


def validate_slurm_executors(slurm_executor):
    """This method will validate slurm executors, we check if partition, qos,
       and cluster fields are valid values by retrieving details from slurm configuration.
       These checks are performed on fields ``partition``, ``qos`` or ``cluster``
       if specified in executor section.

       :param slurm_executor: list of slurm executors defined in loaded buildtest configuration
       :type slurm_executor: dict
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
