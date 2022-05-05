"""
BuildExecutor: manager for test executors
"""

import logging

from buildtest.builders.base import BuilderBase
from buildtest.utils.tools import deep_get


class BaseExecutor:
    """The BaseExecutor is an abstract base class for all executors."""

    type = "base"

    def __init__(self, name, settings, site_configs, timeout=None):
        """Initiate a base executor, meaning we provide a name (also held
        by the BuildExecutor base that holds it) and the loaded dictionary
        of config opts to parse.

        Args:
            name (str): name of executor
            setting (dict): setting for a given executor defined in configuration file
            site_configs (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class
            timeout (str, optional): Test timeout in number of seconds
        """

        self._bashopts = "--norc --noprofile -eo pipefail"
        self._shopts = "--norc --noprofile -eo pipefail"
        self._cshopts = "-e"
        self._zshopts = "-f"
        self.cmd = None
        self.shell = "bash"
        self.logger = logging.getLogger(__name__)
        self.name = name
        self._settings = settings
        self._buildtestsettings = site_configs
        self.timeout = timeout
        self.load()
        self.builders = []

        # the shell type for executors will be bash by default
        # self.shell = "bash"

    def add_builder(self, builder):
        """Add builder object to ``self.builders`` only if its of type BuilderBase"""

        if isinstance(builder, BuilderBase):
            self.builders.append(builder)

    def get_builder(self):
        """Return a list of builders"""
        return self.builders

    def load(self):
        """Load a particular configuration based on the name. This method
        should set defaults for the executor, and will vary based on the
        class.
        """

        self.launcher_opts = self._settings.get("options")
        self.account = (
            self.account
            or self._settings.get("account")
            or deep_get(
                self._buildtestsettings.target_config,
                "executors",
                "defaults",
                "account",
            )
        )
        self.maxpendtime = (
            self.maxpendtime
            or self._settings.get("maxpendtime")
            or deep_get(
                self._buildtestsettings.target_config,
                "executors",
                "defaults",
                "maxpendtime",
            )
        )

    def run(self):
        """The run step basically runs the build. This is run after setup
        so we are sure that the builder is defined. This is also where
        we set the result to return.
        """

    def __str__(self):
        return "%s.%s" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()
