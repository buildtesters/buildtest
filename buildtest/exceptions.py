class BuildTestError(Exception):
    """Class responsible for error handling in buildtest. This is a sub-class
    of Exception class."""

    def __init__(self, msg, *args):
        """ This class is used for printing error message when exception is raised.

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
