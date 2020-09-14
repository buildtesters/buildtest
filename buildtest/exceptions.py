class BuildTestError(Exception):
    """Class responsible for error handling in buildtest. This is a sub-class
    of Exception class."""

    def __init__(self, msg, *args):
        """Constructor Method.

        :param msg: message to print
        :type msg: str,
        :param args:
        :type args:
        """
        if args:
            msg = msg % args
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
