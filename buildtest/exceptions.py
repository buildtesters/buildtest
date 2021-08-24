import yaml


class BuildTestError(Exception):
    """Class responsible for error handling in buildtest. This is a sub-class
    of Exception class."""

    def __init__(self, msg, *args):
        """This class is used for printing error message when exception is raised.

        :param msg: message to print
        :type msg: str, required
        :param args: extra arguments to class
        :type args: list
        """
        self.msg = [msg]
        if args:
            for arg in args:
                self.msg.append(str(arg))

        self.msg = "\n".join(self.msg)

    def __str__(self):
        return repr(self.msg)


class BuildspecError(Exception):
    """raise exception if there is an issue with Buildspec in parsing or building test"""

    def __init__(self, buildspec, msg):
        self.buildspec = buildspec
        self.msg = msg

    def __str__(self):
        return repr(f"[{self.buildspec}]: {self.msg}")


class ExecutorError(Exception):
    """This class raises an error with Executor class and its operation"""


class RuntimeError(Exception):
    """The RuntimeError exception is raised when their is an error running test"""


class ConfigurationError(Exception):
    """This will raise an error related with buildtest configuration file"""

    def __init__(self, config, settings_file, msg):
        self.config = config
        self.settings_file = settings_file
        self.msg = msg
        print(yaml.dump(self.config, default_flow_style=False, sort_keys=False))

    def __str__(self):
        return repr(f"[{self.settings_file}]: {self.msg}")
