import logging
import json
import os
import re

from buildtest.defaults import (
    USER_SETTINGS_FILE,
    DEFAULT_SETTINGS_FILE,
    DEFAULT_SETTINGS_SCHEMA,
)
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_schema, load_recipe
from buildtest.system import Slurm, LSF, Cobalt, PBS, system
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import resolve_path
from buildtest.utils.tools import deep_get
from buildtest.exceptions import BuildTestError


logger = logging.getLogger(__name__)


class BuildtestConfiguration:
    """This class is an interface to buildtest configuration"""

    def __init__(self, settings_file):
        self.file = settings_file
        self.config = load_recipe(settings_file)
        self.systems = self.config["system"].keys()

        # self.target_config stores value for target system. The configuration may define multiple system,
        # but only one system can be active depending on which host buildtest is run
        self.target_config = None
        self._validate()

        self.localexecutors = None
        self.slurmexecutors = None
        self.lsfexecutors = None
        self.cobaltexecutors = None
        self.pbsexecutors = None

        self.get_current_system()

    def get_current_system(self):
        """This method gets current system by setting ``self.target`` by matching ``hostnames`` entry
        in each system list with actual system. We retrieve target hostname and determine which system configuration to use.
        If no system is found we raise an error.
        """
        host_lookup = {}

        # get hostname fqdn
        hostname = " ".join(BuildTestCommand("hostname -f").get_output())

        # for every system record we lookup 'hostnames' entry and apply re.match against current hostname. If found we break from loop
        for name in self.config["system"].keys():
            host_lookup[name] = self.config["system"][name]["hostnames"]

            for host_entry in self.config["system"][name]["hostnames"]:
                if re.match(host_entry, hostname):
                    self.target_config = self.config["system"][name]
                    self.name = name
                    break

        if not self.target_config:
            raise BuildTestError(
                f"Based on current system hostname: {hostname} we cannot find a matching system  {list(self.systems)} based on current hostnames: {host_lookup} "
            )

        if self.target_config["executors"].get("local"):
            self.localexecutors = list(self.target_config["executors"]["local"].keys())

        if self.target_config["executors"].get("slurm"):
            self.slurmexecutors = list(self.target_config["executors"]["slurm"].keys())

        if self.target_config["executors"].get("lsf"):
            self.lsfexecutors = list(self.target_config["executors"]["lsf"].keys())

        if self.target_config["executors"].get("cobalt"):
            self.cobaltexecutors = list(
                self.target_config["executors"]["cobalt"].keys()
            )
        if self.target_config["executors"].get("pbs"):
            self.pbsexecutors = list(
                self.target_config["executors"]["pbs"].keys()
            )
    def get_executors_by_type(self, executor_type):
        """Return list of executor names by given type of executor.
        :param executor_type: type of executor (local, slurm, lsf, cobalt)
        :type executor_type: string
        """
        names = deep_get(self.target_config, "executors", executor_type)
        if not names:
            raise BuildTestError(
                "Cannot fetch executors by type: %s in system: %s ",
                executor_type,
                self.name,
            )

        return list(names.keys())

    def _validate(self):
        """This method validates the site configuration with schema"""

        logger.debug(f"Loading default settings schema: {DEFAULT_SETTINGS_SCHEMA}")
        config_schema = load_schema(DEFAULT_SETTINGS_SCHEMA)

        logger.debug(f"Validating user schema with schema: {DEFAULT_SETTINGS_SCHEMA}")
        custom_validator(recipe=self.config, schema=config_schema)
        logger.debug("Validation was successful")

    def validate_executors(self):
        slurm_executors = deep_get(self.target_config, "executors", "slurm")
        lsf_executors = deep_get(self.target_config, "executors", "lsf")
        cobalt_executors = deep_get(self.target_config, "executors", "cobalt")
        pbs_executors = deep_get(self.target_config, "executors", "pbs")

        if slurm_executors:
            logger.debug("Checking slurm executors")
            self._validate_slurm_executors(slurm_executors)

        if lsf_executors:
            logger.debug("Checking lsf executors")
            self._validate_lsf_executors(lsf_executors)

        if cobalt_executors:
            logger.debug("Checking cobalt executors")
            self._validate_cobalt_executors(cobalt_executors)


        if pbs_executors:
            logger.debug("Checking pbs executors")
            self._validate_pbs_executors(pbs_executors)

        if (
            self.target_config.get("moduletool") != "N/A"
            and self.target_config.get("moduletool") != system.system["moduletool"]
        ):
            raise BuildTestError(
                f"Cannot find modules_tool: {self.target_config('moduletool')} from configuration, please confirm if you have environment-modules or lmod and specify the appropriate tool."
            )

    def _validate_lsf_executors(self, lsf_executors):
        """This method validates all LSF executors. We check if queue is available
        and in ``Open:Active`` state.

        :param lsf_executors: A list of LSF executors to validate
        :type lsf_executors: dict
        """
        lsf = LSF()
        assert hasattr(lsf,"queues")

        queue_list = []
        valid_queue_state = "Open:Active"
        record = lsf.queues["RECORDS"]
        # retrieve all queues from json record
        for name in record:
            queue_list.append(name["QUEUE_NAME"])

        # check all executors have defined valid queues and check queue state.
        for executor in lsf_executors:
            queue = lsf_executors[executor].get("queue")
            # if queue field is defined check if its valid queue
            if queue:
                if queue not in queue_list:
                    raise BuildTestError(
                        f"{lsf_executors[executor]['queue']} not a valid queue!. Please select one of the following queue: {queue_list}"
                    )

                # check queue record for Status
                for name in record:

                    # skip record until we find matching queue
                    if name["QUEUE_NAME"] != queue:
                        continue

                    queue_state = name["STATUS"]
                    # if state not Open:Active we raise error
                    if not queue_state == valid_queue_state:
                        raise BuildTestError(
                            f"{lsf_executors[executor]['queue']} is in state: {queue_state}. It must be in {valid_queue_state} state in order to accept jobs"
                        )

    def _validate_slurm_executors(self, slurm_executor):
        """This method will validate slurm executors, we check if partition, qos,
        and cluster fields are valid values by retrieving details from slurm configuration.
        These checks are performed on fields ``partition``, ``qos`` or ``cluster``
        if specified in executor section.

        :param slurm_executor: list of slurm executors defined in loaded buildtest configuration
        :type slurm_executor: dict
        """

        slurm = Slurm()
        # make sure slurm attributes slurm.partitions, slurm.qos, slurm.clusters are set
        assert hasattr(slurm,"partitions")
        assert hasattr(slurm, "qos")
        assert hasattr(slurm, "clusters")

        for executor in slurm_executor:

            # if 'partition' key defined check if its valid partition
            if slurm_executor[executor].get("partition"):

                if slurm_executor[executor]["partition"] not in slurm.partitions:
                    raise BuildTestError(
                        f"{slurm_executor[executor]['partition']} not a valid partition!. Please select one of the following partitions: {slurm.partitions}"
                    )

                query = (
                    f"sinfo -p {slurm_executor[executor]['partition']} -h -O available"
                )
                cmd = BuildTestCommand(query)
                cmd.execute()
                part_state = "".join(cmd.get_output())
                part_state = part_state.rstrip()
                # check if partition is in 'up' state. If not we raise an error.
                if part_state != "up":
                    raise BuildTestError(
                        f"{slurm_executor[executor]['partition']} is in state: {part_state}. It must be in 'up' state in order to accept jobs"
                    )
            # check if 'qos' key is valid qos
            if (
                slurm_executor[executor].get("qos")
                and slurm_executor[executor].get("qos") not in slurm.qos
            ):
                raise BuildTestError(
                    f"{slurm_executor[executor]['qos']} not a valid qos! Please select one of the following qos: {slurm.qos}"
                )

            # check if 'cluster' key is valid slurm cluster
            if (
                slurm_executor[executor].get("cluster")
                and slurm_executor[executor].get("cluster") not in slurm.clusters
            ):
                raise BuildTestError(
                    f"{slurm_executor[executor]['cluster']} not a valid slurm cluster! Please select one of the following slurm clusters: {slurm.clusters}"
                )

    def _validate_cobalt_executors(self, cobalt_executor):
        """Validate cobalt queue property by running ```qstat -Ql <queue>``. If
        its a non-zero exit code then queue doesn't exist otherwise it is a valid
        queue.
        """

        cobalt = Cobalt()
        assert hasattr(cobalt, "queues")

        for executor in cobalt_executor:
            queue = cobalt_executor[executor].get("queue")
            # if queue property defined in cobalt executor name check if it exists
            if queue not in cobalt.queues:
                raise BuildTestError(
                    f"Queue: {queue} does not exist! To see available queues you can run 'qstat -Ql'"
                )
    def _validate_pbs_executors(self, pbs_executor):
        """Validate pbs queue property by running by checking if queue is found and
           queue is 'enabled' and 'started' which are two properties found in pbs queue
           configuration that can be retrieved using ``qstat -Q -f -F json``. The output is in
           the following format

           $ qstat -Q -f -F json
            {
                "timestamp":1615924938,
                "pbs_version":"19.0.0",
                "pbs_server":"pbs",
                "Queue":{
                    "workq":{
                        "queue_type":"Execution",
                        "total_jobs":0,
                        "state_count":"Transit:0 Queued:0 Held:0 Waiting:0 Running:0 Exiting:0 Begun:0 ",
                        "resources_assigned":{
                            "mem":"0kb",
                            "ncpus":0,
                            "nodect":0
                        },
                        "hasnodes":"True",
                        "enabled":"True",
                        "started":"True"
                    }
                }
            }

        """

        pbs = PBS()
        assert hasattr(pbs,"queues")
        for executor in pbs_executor:
            queue = pbs_executor[executor].get("queue")
            if queue not in pbs.queues:
                raise BuildTestError(f"{queue} not in {pbs.queues}")

            if pbs.queue_summary["Queue"][queue]["enabled"] != "True" or  pbs.queue_summary["Queue"][queue]["started"] != "True":
                print("Queue Configuration")
                print(json.dumps(pbs.queue_summary,indent=2))
                raise BuildTestError(f"{queue} is not enabled or started properly. Please check your queue configuration")


def check_settings(settings_path=None, executor_check=True):
    """Checks all keys in configuration file (settings/config.yml) are valid
    keys and ensure value of each key matches expected type. For some keys
    special logic is taken to ensure values are correct and directory path
    exists. If any error is found buildtest will terminate immediately.

    :param settings_path: Path to buildtest settings file
    :type settings_path: str, optional
    :param executor_check: boolean to control if executor checks are performed
    :type executor_check: bool
    :return: returns an instance object of BuildtestConfiguration
    """

    settings_file = resolve_settings_file(settings_path)
    if not settings_file:
        raise BuildTestError("Cannot detect a buildtest configuration file")

    bc = BuildtestConfiguration(settings_file)

    # only perform executor check if executor_check is True. This is default
    # behavior, this can be disabled only for regression test where executor check
    # such as slurm check are not applicable.
    if executor_check:
        bc.validate_executors()

    return bc


def load_settings(settings_path=None):
    """Load the default settings file if no argument is specified.

    :param settings_path: Path to buildtest settings file
    :type settings_path: str, optional
    """

    if not settings_path:
        settings_path = resolve_settings_file()

    # load the settings file into a schema object
    return load_recipe(settings_path)


def resolve_settings_file(settings_path=None):
    """Returns path to buildtest settings file that should be used. If there
    is a user defined buildtest settings ($HOME/.buildtest/config.yml) it will
    be honored, otherwise default settings from buildtest will be used.
    """

    if settings_path:
        settings_path = resolve_path(settings_path)
        return settings_path

    # if buildtest settings file exist return it otherwise return default file
    if os.path.exists(USER_SETTINGS_FILE):
        return USER_SETTINGS_FILE

    return DEFAULT_SETTINGS_FILE


settings_file = resolve_settings_file()
buildtest_configuration = BuildtestConfiguration(settings_file)
