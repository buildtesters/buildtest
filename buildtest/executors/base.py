"""
BuildExecutor: manager for test executors
"""

import logging


class BaseExecutor:
    """The BaseExecutor is an abstract base class for all executors."""

    type = "base"

    def __init__(self, name, settings, site_configs):
        """Initiate a base executor, meaning we provide a name (also held
        by the BuildExecutor base that holds it) and the loaded dictionary
        of config opts to parse.

        :param name: a name for the base executor and key provided in the configuration file
        :type name: str, required
        :param settings: executor settings from configuration file for a particular executor instance (``local.bash``)
        :type settings: dict, required
        :param site_configs: loaded buildtest configuration
        :type site_configs: instance of SiteConfiguration, required
        """

        self.logger = logging.getLogger(__name__)
        self.name = name
        self._settings = settings
        self._buildtestsettings = site_configs
        self.load()
        self.result = {}

    def load(self):
        """Load a particular configuration based on the name. This method
        should set defaults for the executor, and will vary based on the
        class.
        """

    def run(self):
        """The run step basically runs the build. This is run after setup
        so we are sure that the builder is defined. This is also where
        we set the result to return.
        """

    def __str__(self):
        return "%s.%s" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()
