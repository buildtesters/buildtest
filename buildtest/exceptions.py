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
        self.msg = [msg]
        if args:
            for arg in args:
                self.msg.append(str(arg))

        self.msg = "\n".join(self.msg)

    def __str__(self):
        return repr(self.msg)
