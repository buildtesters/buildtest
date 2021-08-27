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
    """This class is an interface to buildtest configuration"""

    def __init__(self, settings_file=None):
        self._file = settings_file
        self.config = None
        self._name = None
        # self.target_config stores value for target system. The configuration may define multiple system,
        # but only one system can be active depending on which host buildtest is run
        self.target_config = None

        self.localexecutors = []
        self.slurmexecutors = []
        self.lsfexecutors = []
        self.cobaltexecutors = []
        self.pbsexecutors = []

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

        1. command line argument - Must be valid path

        2. User Configuration: $HOME/.buildtest/config.yml

        3. Default Configuration: $BUILDTEST_ROOT/buildtest/settings/config.yml
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
        """This method gets current system by setting ``self.target`` by matching ``hostnames`` entry
        in each system list with actual system. We retrieve target hostname and determine which system configuration to use.
        If no system is found we raise an error.
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
        """This method validates the site configuration with schema"""

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

    def _executor_check(self):
        """Validate executors"""
        self._validate_local_executors()
        self._validate_slurm_executors()
        self._validate_lsf_executors()
        self._validate_cobalt_executors()
        self._validate_pbs_executors()

    def _validate_local_executors(self):
        """Check local executor by verifying the 'shell' types are valid"""
        local_executors = deep_get(self.target_config, "executors", "local")
        if not local_executors:
            return

        # loop over all shell property and see if all shell types are valid path and supported shell. An exception will be raised if there is an issue
        for executor in local_executors:
            name = local_executors[executor]["shell"]

            try:
                Shell(name)
            except BuildTestError as err:
                print(err)
                raise BuildTestError(
                    f"Executor: {executor} failed to validate because 'shell' property points to {name} which is shell type!"
                )

            self.localexecutors.append(executor)

    def _validate_lsf_executors(self):
        """This method validates all LSF executors. We check if queue is available
        and in ``Open:Active`` state.
        """

        lsf_executors = deep_get(self.target_config, "executors", "lsf")
        if not lsf_executors:
            return

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

            queue = lsf_executors[executor].get("queue")
            # if queue field is defined check if its valid queue
            if queue:
                if queue not in queue_list:
                    raise ConfigurationError(
                        self.config,
                        self.file,
                        f"{lsf_executors[executor]['queue']} not a valid queue!. Please select one of the following queue: {queue_list}",
                    )

                # check queue record for Status
                for name in record:

                    # skip record until we find matching queue
                    if name["QUEUE_NAME"] != queue:
                        continue

                    queue_state = name["STATUS"]
                    # if state not Open:Active we raise error
                    if not queue_state == valid_queue_state:
                        raise ConfigurationError(
                            self.config,
                            self.file,
                            f"{lsf_executors[executor]['queue']} is in state: {queue_state}. It must be in {valid_queue_state} state in order to accept jobs",
                        )

            self.lsfexecutors.append(executor)

    def _validate_slurm_executors(self):
        """This method will validate slurm executors, we check if partition, qos,
        and cluster fields are valid values by retrieving details from slurm configuration.
        These checks are performed on fields ``partition``, ``qos`` or ``cluster``
        if specified in executor section.
        """

        slurm_executor = deep_get(self.target_config, "executors", "slurm")
        if not slurm_executor:
            return

        slurm = Slurm()

        for executor in slurm_executor:
            # if 'partition' key defined check if its valid partition
            if slurm_executor[executor].get("partition"):

                if slurm_executor[executor]["partition"] not in slurm.partitions:
                    raise ConfigurationError(
                        self.config,
                        self.file,
                        f"{slurm_executor[executor]['partition']} not a valid partition!. Please select one of the following partitions: {slurm.partitions}",
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
                    raise ConfigurationError(
                        self.config,
                        self.file,
                        f"{slurm_executor[executor]['partition']} is in state: {part_state}. It must be in 'up' state in order to accept jobs",
                    )
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
                raise ConfigurationError(
                    self.config,
                    self.file,
                    f"{slurm_executor[executor]['cluster']} not a valid slurm cluster! Please select one of the following slurm clusters: {slurm.clusters}",
                )

            self.slurmexecutors.append(executor)

    def _validate_cobalt_executors(self):
        """Validate cobalt queue property by running ```qstat -Ql <queue>``. If
        its a non-zero exit code then queue doesn't exist otherwise it is a valid
        queue.
        """

        cobalt_executor = deep_get(self.target_config, "executors", "cobalt")
        if not cobalt_executor:
            return

        cobalt = Cobalt()
        assert hasattr(cobalt, "queues")

        for executor in cobalt_executor:
            queue = cobalt_executor[executor].get("queue")
            # if queue property defined in cobalt executor name check if it exists
            if queue not in cobalt.queues:
                raise ConfigurationError(
                    self.config,
                    self.file,
                    f"Queue: {queue} does not exist! To see available queues you can run 'qstat -Ql'",
                )

            self.cobaltexecutors.append(executor)

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

        pbs = PBS()
        assert hasattr(pbs, "queues")
        for executor in pbs_executor:
            queue = pbs_executor[executor].get("queue")
            if queue not in pbs.queues:
                raise ConfigurationError(
                    self.config, self.file, f"{queue} not in {pbs.queues}"
                )

            if (
                pbs.queue_summary["Queue"][queue]["enabled"] != "True"
                or pbs.queue_summary["Queue"][queue]["started"] != "True"
            ):
                print("Queue Configuration")
                print(json.dumps(pbs.queue_summary, indent=2))
                raise ConfigurationError(
                    self.config,
                    self.file,
                    f"{queue} is not enabled or started properly. Please check your queue configuration",
                )

            self.pbsexecutors.append(executor)
