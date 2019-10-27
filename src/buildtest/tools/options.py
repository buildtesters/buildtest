"""
Overrides buildtest configuration via environment variable or command options
"""

import os
from distutils.util import strtobool
from buildtest.tools.config import config_opts
from buildtest.tools.log import BuildTestError

def override_configuration():
    """This method override buildtest options by environment variables """

    bool_config_override("BUILDTEST_BINARY")
    bool_config_override("BUILDTEST_MODULE_FORCE_PURGE")


    if os.environ.get('BUILDTEST_SHELL'):
        config_opts['BUILDTEST_SHELL']=os.environ['BUILDTEST_SHELL']

    if os.environ.get('BUILDTEST_SPIDER_VIEW'):
        config_opts['BUILDTEST_SPIDER_VIEW']=os.environ[
            'BUILDTEST_SPIDER_VIEW']

    if os.environ.get('BUILDTEST_PARENT_MODULE_SEARCH'):
        config_opts['BUILDTEST_PARENT_MODULE_SEARCH']=os.environ[
            'BUILDTEST_PARENT_MODULE_SEARCH']

    if os.environ.get('BUILDTEST_SUCCESS_THRESHOLD'):
        threshold = float(os.environ.get('BUILDTEST_SUCCESS_THRESHOLD'))

        if threshold >= 0.0 and threshold <= 1.0:
            config_opts['BUILDTEST_SUCCESS_THRESHOLD']=threshold

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
            values = ["y","yes","t","true","on",1,"n","f","false","off",0]
            raise BuildTestError(f"Must be one of the following {values}")