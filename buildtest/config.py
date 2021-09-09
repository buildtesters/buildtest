import json
import logging
import re

from buildtest.defaults import (
    DEFAULT_SETTINGS_FILE,
    DEFAULT_SETTINGS_SCHEMA,
    USER_SETTINGS_FILE,
)
from buildtest.exceptions import BuildTestError, ConfigurationError
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_recipe, load_schema
from buildtest.system import LSF, PBS, Cobalt, Slurm, system
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import resolve_path
from buildtest.utils.shell import Shell
from buildtest.utils.tools import deep_get

logger = logging.getLogger(__name__)


class SiteConfiguration:
    """This class is an interface to buildtest configuration

    Attributes:
        _file (str): Path to configuration file
        config (dict): Loaded configuration fille
        target_config (dict): Loaded configuration file for a particular system
        disabled_executors (list): A list of disabled executors when checking executors
        invalid_executors (list): A list of invalid executors when checking executors
        valid_executors (dict): A dict containing executors that are valid for each executor type.
    """

    def __init__(self, settings_file=None):
        """The initializer will declare class variables in its initial state and resolve path to
        configuration file. Once file is resolved we will load the configuration using :func:`load`.

        Args:
            settings_file (str, optional): path to buildtest configuration file

        """

        self._file = settings_file
        self.config = None
        self._name = None
        # self.target_config stores value for target system. The configuration may define multiple system,
        # but only one system can be active depending on which host buildtest is run
        self.target_config = None

        self.disabled_executors = []
        self.invalid_executors = []
        self.valid_executors = {
            "local": {},
            "slurm": {},
            "lsf": {},
            "pbs": {},
            "cobalt": {},
        }

        self.resolve()
        self.load()

    def load(self):
        """Loads configuration file"""
        self.config = load_recipe(self._file)

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, path):
        self._file = path

    def resolve(self):
        """This method will resolve path to configuration file. The order of precedence is as follows:

        1. command line argument via ``buildtest --config <path>``
        2. User Configuration: **$HOME/.buildtest/config.yml**
        3. Default Configuration: **$BUILDTEST_ROOT/buildtest/settings/config.yml**
        """

        self._file = (
            resolve_path(self._file)
            or resolve_path(USER_SETTINGS_FILE)
            or DEFAULT_SETTINGS_FILE
        )

    def name(self):
        """Return name of matched system from configuration file"""
        return self._name

    def detect_system(self):
        """This method detects which system configuration to use by checking target hostname with list of hostname entries defined in ``hostnames`` property. If there
        is a match we set ``self._name`` to map to system name and load the target configuration by setting ``self.target_config`` to the desired system configuration.

        If no system is found we raise an exception.

        Raises:
            ConfigurationError: If there is no matching system
        """

        self.systems = list(self.config["system"].keys())

        host_lookup = {}

        # get hostname fqdn
        cmd = BuildTestCommand("hostname -f")
        cmd.execute()
        hostname = " ".join(cmd.get_output())

        # for every system record we lookup 'hostnames' entry and apply re.match against current hostname. If found we break from loop
        for name in self.systems:
            host_lookup[name] = self.config["system"][name]["hostnames"]

            for host_entry in self.config["system"][name]["hostnames"]:
                if re.match(host_entry, hostname):
                    self.target_config = self.config["system"][name]
                    self._name = name
                    break

        if not self.target_config:
            raise ConfigurationError(
                self.config,
                self.file,
                f"Based on current system hostname: {hostname} we cannot find a matching system  {list(self.systems)} based on current hostnames: {host_lookup} ",
            )
        if self.target_config["executors"].get("local"):
            self.localexecutors = list(self.target_config["executors"]["local"].keys())

    def validate(self, validate_executors=True):
        """This method validates the site configuration with schema and checks executor setting.

        Args:
             validate_executors (bool): Check executor settings. This is the default behavior but can be disabled
        """

        logger.debug(f"Loading default settings schema: {DEFAULT_SETTINGS_SCHEMA}")
        config_schema = load_schema(DEFAULT_SETTINGS_SCHEMA)

        logger.debug(
            f"Validating configuration file with schema: {DEFAULT_SETTINGS_SCHEMA}"
        )
        custom_validator(recipe=self.config, schema=config_schema)
        logger.debug("Validation was successful")

        if validate_executors:
            self._executor_check()

        if (
            self.target_config.get("moduletool") != "N/A"
            and self.target_config.get("moduletool") != system.system["moduletool"]
        ):
            raise ConfigurationError(
                self.config,
                self.file,
                f"Cannot find modules_tool: {self.target_config['moduletool']} from configuration, please confirm if you have environment-modules or lmod and specify the appropriate tool.",
            )
        """
        if self.invalid_executors:
            raise ConfigurationError(
                self.config,
                self.file,
                f"The following executors are invalid: {self.invalid_executors}",
            )
        """

    def _executor_check(self):
        """Validate executors"""
        self._validate_local_executors()
        self._validate_slurm_executors()
        self._validate_lsf_executors()
        self._validate_cobalt_executors()
        self._validate_pbs_executors()

    def _validate_local_executors(self):
        """Check local executor by verifying the 'shell' types are valid"""
        executor_type = "local"

        local_executors = deep_get(self.target_config, "executors", "local")
        if not local_executors:
            return

        # loop over all shell property and see if all shell types are valid path and supported shell. An exception will be raised if there is an issue
        for executor in local_executors:
            name = local_executors[executor]["shell"]

            if local_executors[executor].get("disable"):
                self.disabled_executors.append(
                    f"{self.name()}.{executor_type}.{executor}"
                )
                continue

            try:
                Shell(name)
            except BuildTestError as err:
                self.invalid_executors.append(
                    f"{self.name()}.{executor_type}.{executor}"
                )
                logger.error(err)
                continue

            self.valid_executors[executor_type][
                f"{self.name()}.{executor_type}.{executor}"
            ] = {"setting": local_executors[executor]}

    def _validate_lsf_executors(self):
        """This method validates all LSF executors. We check if queue is available
        and in ``Open:Active`` state.
        """

        lsf_executors = deep_get(self.target_config, "executors", "lsf")
        if not lsf_executors:
            return

        executor_type = "lsf"

        lsf = LSF()
        assert hasattr(lsf, "queues")

        queue_list = []
        valid_queue_state = "Open:Active"
        record = lsf.queues["RECORDS"]
        # retrieve all queues from json record
        for name in record:
            queue_list.append(name["QUEUE_NAME"])

        # check all executors have defined valid queues and check queue state.
        for executor in lsf_executors:

            if lsf_executors[executor].get("disable"):
                self.disabled_executors.append(
                    f"{self.name()}.{executor_type}.{executor}"
                )
                continue

            queue = lsf_executors[executor].get("queue")
            # if queue field is defined check if its valid queue
            if queue:
                if queue not in queue_list:
                    self.invalid_executors.append(
                        f"{self.name()}.{executor_type}.{executor}"
                    )
                    logger.error(
                        f"'{queue}' is invalid LSF queue. Please select one of the following queues: {queue_list}"
                    )
                    continue

                # check queue record for Status
                for name in record:

                    # skip record until we find matching queue
                    if name["QUEUE_NAME"] != queue:
                        continue

                    queue_state = name["STATUS"]
                    # if state not Open:Active we raise error
                    if not queue_state == valid_queue_state:
                        self.invalid_executors.append(
                            f"{self.name()}.{executor_type}.{executor}"
                        )
                        logger.error(
                            f"'{queue}' is in state: {queue_state}. It must be in {valid_queue_state} state in order to accept jobs"
                        )
                        break

            self.valid_executors[executor_type][
                f"{self.name()}.{executor_type}.{executor}"
            ] = {"setting": lsf_executors[executor]}

    def _validate_slurm_executors(self):
        """This method will validate slurm executors, we check if partition, qos,
        and cluster fields are valid values by retrieving details from slurm configuration.
        These checks are performed on fields ``partition``, ``qos`` or ``cluster``
        if specified in executor section.
        """

        slurm_executor = deep_get(self.target_config, "executors", "slurm")
        if not slurm_executor:
            return

        executor_type = "slurm"
        slurm = Slurm()

        for executor in slurm_executor:

            if slurm_executor[executor].get("disable"):
                self.disabled_executors.append(
                    f"{self.name()}.{executor_type}.{executor}"
                )
                continue

            # if 'partition' key defined check if its valid partition
            if slurm_executor[executor].get("partition"):

                if slurm_executor[executor]["partition"] not in slurm.partitions:
                    self.invalid_executors(f"{self.name()}.{executor_type}.{executor}")
                    logger.error(
                        f"executor - {executor} has invalid partition name '{slurm_executor[executor]['partition']}'. Please select one of the following partitions: {slurm.partitions}"
                    )
                    continue

                query = (
                    f"sinfo -p {slurm_executor[executor]['partition']} -h -O available"
                )
                cmd = BuildTestCommand(query)
                cmd.execute()
                part_state = "".join(cmd.get_output())
                part_state = part_state.rstrip()
                # check if partition is in 'up' state. If not we raise an error.
                if part_state != "up":
                    self.invalid_executors(f"{self.name()}.{executor_type}.{executor}")
                    logger.error(
                        f"partition - {slurm_executor[executor]['partition']} is in state: {part_state}. It must be in 'up' state in order to accept jobs"
                    )
                    continue

            """ disable qos check for now. Issue with 'regular' qos at Cori where it maps to 'regular_hsw' partition while 'regular' is the valid qos name' 
            # check if 'qos' key is valid qos
            if (
                slurm_executor[executor].get("qos")
                and slurm_executor[executor].get("qos") not in slurm.qos
            ):
                raise ConfigurationError(
                    self.config,
                    self.file,
                    f"{slurm_executor[executor]['qos']} not a valid qos! Please select one of the following qos: {slurm.qos}",
                )
            """

            # check if 'cluster' key is valid slurm cluster
            if (
                slurm_executor[executor].get("cluster")
                and slurm_executor[executor].get("cluster") not in slurm.clusters
            ):
                self.invalid_executors(f"{self.name()}.{executor_type}.{executor}")
                logger.error(
                    f"executor - {executor} has invalid slurm cluster - {slurm_executor[executor]['cluster']}. Please select one of the following slurm clusters: {slurm.clusters}"
                )
                continue

            self.valid_executors[executor_type][
                f"{self.name()}.{executor_type}.{executor}"
            ] = {"setting": slurm_executor[executor]}

    def _validate_cobalt_executors(self):
        """Validate cobalt queue property by running ```qstat -Ql <queue>``. If
        its a non-zero exit code then queue doesn't exist otherwise it is a valid
        queue.
        """

        cobalt_executor = deep_get(self.target_config, "executors", "cobalt")
        if not cobalt_executor:
            return

        executor_type = "cobalt"

        cobalt = Cobalt()
        assert hasattr(cobalt, "queues")

        for executor in cobalt_executor:

            if cobalt_executor[executor].get("disable"):
                self.disabled_executors.append(
                    f"{self.name()}.{executor_type}.{executor}"
                )
                continue

            queue = cobalt_executor[executor].get("queue")
            # if queue property defined in cobalt executor name check if it exists
            if queue not in cobalt.queues:
                logger.error(
                    f"Cobalt queue '{queue}' does not exist. Available Cobalt queues: {cobalt.queues} "
                )
                continue

            self.valid_executors[executor_type][
                f"{self.name()}.{executor_type}.{executor}"
            ] = {"setting": cobalt_executor[executor]}

    def _validate_pbs_executors(self):
        """Validate pbs queue property by running by checking if queue is found and
        queue is 'enabled' and 'started' which are two properties found in pbs queue
        configuration that can be retrieved using ``qstat -Q -f -F json``. The output is in
        the following format

        .. code-block:: console

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

        pbs_executor = deep_get(self.target_config, "executors", "pbs")
        if not pbs_executor:
            return

        executor_type = "pbs"

        pbs = PBS()
        assert hasattr(pbs, "queues")
        for executor in pbs_executor:

            if pbs_executor[executor].get("disable"):
                self.disabled_executors.append(f"{self.name()}.pbs.{executor}")
                continue

            queue = pbs_executor[executor].get("queue")
            if queue not in pbs.queues:
                self.invalid_executors.append(f"{self.name()}.pbs.{queue}")
                logger.error(
                    f"PBS queue - '{queue}' not in list of available queues: {pbs.queues} "
                )
                continue

            if (
                pbs.queue_summary["Queue"][queue]["enabled"] != "True"
                or pbs.queue_summary["Queue"][queue]["started"] != "True"
            ):

                self.invalid_executors.append(f"{self.name()}.pbs.{queue}")
                logger.info("Queue configuration")
                logger.info(json.dumps(pbs.queue_summary, indent=2))
                logger.error(
                    f"[{self.file}]: '{queue}' not 'enabled' or 'started' properly."
                )
                continue

            self.valid_executors[executor_type][
                f"{self.name()}.{executor_type}.{executor}"
            ] = {"setting": pbs_executor[executor]}
