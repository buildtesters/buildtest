import logging
import re
import socket

from buildtest.defaults import (
    DEFAULT_SETTINGS_FILE,
    DEFAULT_SETTINGS_SCHEMA,
    USER_SETTINGS_FILE,
    console,
)
from buildtest.exceptions import BuildTestError, ConfigurationError
from buildtest.scheduler.detection import LSF, PBS, Slurm, Torque
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_recipe, load_schema
from buildtest.utils.file import resolve_path
from buildtest.utils.shell import Shell
from buildtest.utils.tools import deep_get

logger = logging.getLogger(__name__)


class SiteConfiguration:
    """This class is an interface to buildtest configuration"""

    def __init__(self, settings_file=None, verbose=None):
        """The initializer will declare class variables in its initial state and resolve path to
        configuration file. Once file is resolved we will load the configuration using :func:`load`.

        Args:
            settings_file (str, optional): path to buildtest configuration file

        """
        self.verbose = verbose
        self._file = settings_file
        self.config = None
        self._name = None
        # self.target_config stores value for target system. The configuration may define multiple system,
        # but only one system can be active depending on which host buildtest is run
        self.target_config = None

        self.disabled_executors = []
        self.invalid_executors = []
        self.all_executors = []
        self.valid_executors = {
            "local": {},
            "slurm": {},
            "lsf": {},
            "pbs": {},
            "torque": {},
            "container": {},
        }

        self.resolve()
        self.load()

    def load(self):
        """Loads configuration file"""
        self.config = load_recipe(self._file)
        if self.verbose:
            console.print("Loading configuration file ... COMPLETE", style="bold blue")

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
        logger.debug(
            f"List of available systems: {self.systems} found in configuration file"
        )
        host_lookup = {}

        # get hostname fqdn
        hostname = socket.getfqdn()

        if self.verbose:
            console.print(f"Detected hostname: {hostname}", style="bold blue")

        # for every system record we lookup 'hostnames' entry and apply re.match against current hostname. If found we break from loop
        for name in self.systems:
            host_lookup[name] = self.config["system"][name]["hostnames"]

            logger.debug(
                f"Checking hostname: {hostname} in system: '{name}' with hostnames: {host_lookup[name]}"
            )
            for host_entry in self.config["system"][name]["hostnames"]:
                if re.fullmatch(host_entry, hostname):
                    self.target_config = self.config["system"][name]
                    self._name = name
                    logger.info(
                        f"Found matching system: {name} based on hostname: {hostname}"
                    )
                    break

        if not self.target_config:
            raise ConfigurationError(
                self.config,
                self.file,
                f"Based on current system hostname: {hostname} we cannot find a matching system  {list(self.systems)} based on current hostnames: {host_lookup} ",
            )

    def validate(self, moduletool=None):
        """This method validates the site configuration with schema.

        Args:
             moduletool (bool, optional): Check whether module system (Lmod, environment-modules) match what is specified in configuration file. Valid options are ``Lmod``, ``environment-modules``
        """

        logger.debug(f"Loading default settings schema: {DEFAULT_SETTINGS_SCHEMA}")
        config_schema = load_schema(DEFAULT_SETTINGS_SCHEMA)

        logger.debug(
            f"Validating configuration file with schema: {DEFAULT_SETTINGS_SCHEMA}"
        )
        custom_validator(recipe=self.config, schema=config_schema)
        if self.verbose:
            console.print(
                "Validating configuration file ... COMPLETE", style="bold blue"
            )
        logger.debug("Validation was successful")

        self._executor_check()

        if (
            self.target_config.get("moduletool") != "none"
            and self.target_config.get("moduletool") != moduletool
        ):
            raise ConfigurationError(
                self.config,
                self.file,
                f"There is a module tool mismatch, we have detected '{moduletool}' but configuration property 'moduletool' specifies  '{self.target_config['moduletool']}'",
            )

    def _executor_check(self):
        """Validate executors"""

        if self.verbose:
            console.print("Initiating executor check ...", style="bold blue")

        self._validate_local_executors()
        self._validate_slurm_executors()
        self._validate_lsf_executors()
        self._validate_pbs_executors()
        self._validate_torque_executors()
        self._validate_container_executors()

        for executor_type in self.target_config["executors"]:
            if executor_type == "defaults":
                continue

            for name in self.target_config["executors"][executor_type]:
                self.all_executors.append(f"{self.name()}.{executor_type}.{name}")

        if self.verbose:
            console.print(
                f"We have found the following executors: {self.all_executors}",
                style="bold blue",
            )

    def get_all_executors(self):
        """Return list of all executors"""
        return self.all_executors

    def is_executor_disabled(self, executor):
        if executor.get("disable"):
            return True

        return False

    def _validate_container_executors(self):
        executor_names = deep_get(self.target_config, "executors", "container")
        if not executor_names:
            return
        for executor in executor_names:
            executor_name = f"{self.name()}.container.{executor}"
            if self.is_executor_disabled(executor_names[executor]):
                self.disabled_executors.append(executor_name)
                continue

            self.valid_executors["container"][executor_name] = {
                "setting": executor_names[executor]
            }

    def _validate_local_executors(self):
        """Check local executor by verifying the 'shell' types are valid"""
        executor_type = "local"

        local_executors = deep_get(self.target_config, "executors", "local")
        if not local_executors:
            return

        # loop over all shell property and see if all shell types are valid path and supported shell. An exception will be raised if there is an issue
        for executor in local_executors:
            name = local_executors[executor]["shell"]

            executor_name = f"{self.name()}.{executor_type}.{executor}"

            if self.is_executor_disabled(local_executors[executor]):
                self.disabled_executors.append(executor_name)
                continue

            try:
                Shell(name)
            except BuildTestError as err:
                self.invalid_executors.append(executor_name)
                logger.error(err)
                continue

            self.valid_executors[executor_type][executor_name] = {
                "setting": local_executors[executor]
            }

    def _validate_lsf_executors(self):
        """This method validates all LSF executors. We check if queue is available
        and in ``Open:Active`` state.
        """

        lsf_executors = deep_get(self.target_config, "executors", "lsf")
        if not lsf_executors:

            if self.verbose:
                console.print(
                    "No LSF executors found in configuration file", style="bold blue"
                )
            return

        executor_type = "lsf"

        lsf = LSF(custom_dirs=deep_get(self.target_config, "paths", "lsf"))
        if not lsf.active():
            return

        # check all executors have defined valid queues and check queue state.
        for executor in lsf_executors:
            executor_name = f"{self.name()}.{executor_type}.{executor}"
            if self.is_executor_disabled(lsf_executors[executor]):
                self.disabled_executors.append(executor_name)
                continue

            if not lsf.validate_queue(executor=lsf_executors[executor]):
                self.invalid_executors.append(executor_name)
                continue

            self.valid_executors[executor_type][executor_name] = {
                "setting": lsf_executors[executor]
            }

    def _validate_slurm_executors(self):
        """This method will validate slurm executors, we check if partition, qos,
        and cluster fields are valid values by retrieving details from slurm configuration.
        These checks are performed on fields ``partition``, ``qos`` or ``cluster``
        if specified in executor section.
        """

        slurm_executor = deep_get(self.target_config, "executors", "slurm")
        if not slurm_executor:

            if self.verbose:
                console.print(
                    "No SLURM executors found in configuration file", style="bold blue"
                )

            return

        executor_type = "slurm"
        slurm = Slurm(custom_dirs=deep_get(self.target_config, "paths", "slurm"))

        if not slurm.active():
            return

        slurm_partitions = slurm.partitions()
        slurm_qos = slurm.qos()
        slurm_clusters = slurm.clusters()
        logger.debug(f"SLURM Partitions: {slurm_partitions}")
        logger.debug(f"SLURM QOS: {slurm_qos}")
        logger.debug(f"SLURM Clusters: {slurm_clusters}")
        for executor in slurm_executor:
            executor_name = f"{self.name()}.{executor_type}.{executor}"

            if self.is_executor_disabled(slurm_executor[executor]):
                self.disabled_executors.append(executor_name)
                continue
            if slurm_executor[executor].get("partition"):
                if not slurm.validate_partition(slurm_executor[executor]):
                    self.invalid_executors.append(executor_name)
                    continue
            if slurm_executor[executor].get("cluster"):
                if not slurm.validate_cluster(executor, slurm_executor[executor]):
                    self.invalid_executors.append(executor_name)
                    continue

            if slurm_executor[executor].get("qos"):
                if not slurm.validate_qos(executor, slurm_executor[executor]):
                    self.invalid_executors.append(executor_name)
                    continue

            self.valid_executors[executor_type][executor_name] = {
                "setting": slurm_executor[executor]
            }

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

            if self.verbose:
                console.print(
                    "No PBS executors found in configuration file", style="bold blue"
                )

            return

        executor_type = "pbs"

        pbs = PBS(custom_dirs=deep_get(self.target_config, "paths", "pbs"))
        if not pbs.active():
            return

        for executor in pbs_executor:
            executor_name = f"{self.name()}.{executor_type}.{executor}"

            if self.is_executor_disabled(pbs_executor[executor]):
                self.disabled_executors.append(executor_name)
                continue

            queue = pbs_executor[executor].get("queue")
            if not pbs.validate_queue(queue):
                self.invalid_executors.append(executor_name)
                continue

            self.valid_executors[executor_type][executor_name] = {
                "setting": pbs_executor[executor]
            }

    def _validate_torque_executors(self):

        torque_executor = deep_get(self.target_config, "executors", "torque")
        if not torque_executor:

            if self.verbose:
                console.print(
                    "No PBS/Torque executors found in configuration file",
                    style="bold blue",
                )

            return

        executor_type = "torque"

        torque = Torque(custom_dirs=deep_get(self.target_config, "paths", "torque"))
        if not torque.active():
            return

        for executor in torque_executor:
            executor_name = f"{self.name()}.{executor_type}.{executor}"

            if self.is_executor_disabled(torque_executor[executor]):
                self.disabled_executors.append(executor_name)
                continue

            if not torque.validate_queue(torque_executor[executor]):
                self.invalid_executors.append(executor_name)
                continue

            self.valid_executors[executor_type][executor_name] = {
                "setting": torque_executor[executor]
            }

    def get_profile(self, profile_name):
        """Return configuration for a given profile name

        Args:
            profile_name (str): name of profile to retrieve

        Returns:
            dict: dictionary containing a profile configuration
        """

        if not self.target_config.get("profiles"):
            raise BuildTestError(
                "There are no profiles defined in configuration file, please consider creating a profile using the --save-profile option"
            )

        if not self.target_config["profiles"].get(profile_name):
            raise BuildTestError(
                f"Unable to find profile: {profile_name} in configuration file. List of available profiles are: {list(self.target_config['profiles'].keys())}"
            )

        return self.target_config["profiles"][profile_name]
