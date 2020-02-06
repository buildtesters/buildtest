"""
Overrides buildtest configuration via environment variable or command options
"""

import os
from distutils.util import strtobool
from buildtest.tools.config import config_opts
from buildtest.tools.log import BuildTestError

def bool_config_override(key):
    """Override boolean configuration via environment variable. Executes a
    "try" block to check if value of environment variable resolve to ``True`` or ``False``
    statement using **strtobool()**. Catches exception of type ``ValueError`` and raises
    exception **BuildTestError()**.

    :param key: environment variable name
    :type key: str,required
    :raises BuildTestError: Prints custom exception message
    :rtype: raise exception on failure
    """
    if os.environ.get(key):
        try:
            truth_value = strtobool(os.environ[key])
            if truth_value == 1:
                config_opts[key] = True
            else:
                config_opts[key] = False
        except ValueError:
            values = ["y", "yes", "t", "true", "on", 1, "n", "f", "false", "off", 0]
            raise BuildTestError(f"Must be one of the following {values}")
