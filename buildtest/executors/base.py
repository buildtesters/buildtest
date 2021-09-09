"""
BuildExecutor: manager for test executors
"""

import logging

from buildtest.buildsystem.base import BuilderBase


class BaseExecutor:
    """The BaseExecutor is an abstract base class for all executors."""

    type = "base"

    def __init__(self, name, settings, site_configs):
        """Initiate a base executor, meaning we provide a name (also held
        by the BuildExecutor base that holds it) and the loaded dictionary
        of config opts to parse.

        Args:
            name (str): name of executor
            setting (dict): setting for a given executor defined in configuration file
            site_configs (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class
        """

        self.logger = logging.getLogger(__name__)
        self.name = name
        self._settings = settings
        self._buildtestsettings = site_configs
        self.load()
        self.builders = []

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

    def run(self):
        """The run step basically runs the build. This is run after setup
        so we are sure that the builder is defined. This is also where
        we set the result to return.
        """

    def __str__(self):
        return "%s.%s" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()
