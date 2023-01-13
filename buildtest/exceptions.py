import yaml


class BuildTestError(Exception):
    """Class responsible for error handling in buildtest. This is a sub-class
    of Exception class."""

    def __init__(self, msg, *args):
        """This class is used for printing error message when exception is raised.

        Args:
            msg (str): message to print
            *args (list): extra arguments to class for printing message
        """
        self.msg = [msg]
        if args:
            for arg in args:
                self.msg.append(str(arg))

        self.msg = "\n".join(self.msg)

    def __str__(self):
        return repr(self.msg)


class BuildspecError(Exception):
    """Exception if there is an issue with parsing a Buildspec or building test"""

    def __init__(self, msg, buildspec=None):

        self.msg = msg
        if buildspec:
            self.msg = f"[{buildspec}]: {msg}"

    def get_exception(self):
        return repr(self.msg)

    """
    def __str__(self):
        if not self.buildspec:
            return f"{self.msg}"

        return repr(f"[{self.buildspec}]: {self.msg}")

    """


class InvalidBuildspec(BuildspecError):
    """This class raises exception for InvalidBuildspec"""


class InvalidBuildspecSchemaType(BuildspecError):
    """This exception is raised when buildspec contains invalid schema 'type'"""


class InvalidBuildspecExecutor(BuildspecError):
    """This exception is raised when there is invalid 'executor' in buildspec"""


class ExecutorError(Exception):
    """This class raises an error with Executor class and its operation"""


class RuntimeFailure(Exception):
    """The RuntimeFailure exception is raised when their is an error running test"""


class ConfigurationError(Exception):
    """ConfigurationError is raised when their is an issue with buildtest configuration file"""

    def __init__(self, config, settings_file, msg):
        self.config = config
        self.settings_file = settings_file
        self.msg = msg
        print(yaml.dump(self.config, default_flow_style=False, sort_keys=False))

    def __str__(self):
        return repr(f"[{self.settings_file}]: {self.msg}")
