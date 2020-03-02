from buildtest.tools.system import BuildTestCommand


def get_all_collections():
    """Get all Lmod user collections that is retrieved by running ``module -t savelist``.

     :return: Return all module collections
     :rtype: list
     """

    collections = "module -t savelist"
    cmd = BuildTestCommand()
    cmd.execute(collections)
    # The output is captured in STDERR stream.
    out = cmd.get_error().split()

    return out


class Module:
    """Class declaration for Module class"""

    def __init__(self, modules=None, purge=True, force=False, debug=False):
        """Initialize method for Module class.

        :param modules: list of modules
        :param purge: boolean to control whether to purge modules before loading
        :param force: boolean to control whether to force purge modules before loading
        :param debug: debug mode for troubleshooting

        :type modules: list
        :type purge: bool
        :type force: bool
        :type debug: bool
        """
        self.debug = debug
        self.modules = modules

        # when no modules are passed into initializer, just return immediately
        if self.modules is None:
            return

        # catch all exceptions to argument modules. Must be of type list or string.
        if (not isinstance(modules, list)) and (not isinstance(modules, str)):
            raise TypeError(
                f"Expecting of type 'list' or 'string' for argument modules. Got of type {type(modules)}"
            )

        # if argument is a string, than use space as delimeter to get list of all modules.
        if isinstance(modules, str):
            self.modules = modules.split(" ")

        # building actual command. Note that we are doing command chaining when loading modules
        self.module_load_cmd = [f"module load {x} && " for x in self.modules]

        # remove last '&&' from module load command
        self.module_load_cmd[-1] = self.module_load_cmd[-1].replace("&&", "")

        if purge:
            # force purge modules before loading modules. Used when dealing with sticky modules
            if force:
                self.module_load_cmd = [
                    "module --force purge && "
                ] + self.module_load_cmd
            # purge modules before loading modules.
            else:
                self.module_load_cmd = ["module purge &&"] + self.module_load_cmd

    def get_command(self):
        """ Get the actual module load command that can be used to load the given modules.

        :return: return the actual module load command
        :rtype: str
        """

        return " ".join(self.module_load_cmd)

    def test_modules(self):
        """ Test all specified modules by loading them using ``module load``.

        :return: return code of ``module load`` command
        :rtype: int
        """
        cmd_executed = self.get_command()

        cmd = BuildTestCommand()
        cmd.execute(cmd_executed)
        ret = cmd.returnCode()

        # print executed command for debugging
        if self.debug:
            print(f"[DEBUG] Executing module command: {cmd_executed}")
            print(f"[DEBUG] Return Code: {ret}")

        return ret

    def save(self, collection="default"):
        """Save active modules into a module collection.

        :param collection: collection name to save modules. If none specified, ``default`` is the collection.
        :type collection: str
        """

        # raise TypeError exception if collection is not a string type since that is required
        # when working with module collection
        if not isinstance(collection, str):
            raise TypeError(f"Type Error: {collection} is not of type string")

        module_save_cmd = f"{self.get_command()} && module save {collection}"
        cmd = BuildTestCommand()
        cmd.execute(module_save_cmd)

        # For some odd reason, the output of module save gets passed to STDERR stream instead of STDOUT.
        out = cmd.get_error()
        ret = cmd.returnCode()

        # print executed command for debugging
        if self.debug:
            print(f"[DEBUG] Executing module command: {module_save_cmd}")
            print(f"[DEBUG] Return Code: {ret}")

        print(f"Saving modules {self.modules} to module collection name: {collection}")
        print(out)

    def describe(self, collection="default"):
        """Show content of a module collection.

        :param collection: name of module collection
        :type collection: str
        """

        # raise TypeError exception if collection is not a string type since that is required
        # when working with module collection
        if not isinstance(collection, str):
            raise TypeError(f"Type Error: {collection} is not of type string")

        module_describe_cmd = f"module describe {collection}"
        cmd = BuildTestCommand()
        cmd.execute(module_describe_cmd)
        ret = cmd.returnCode()

        # For some odd reason, the output of module save gets passed to STDERR stream instead of STDOUT.
        out = cmd.get_error()

        # print executed command for debugging
        if self.debug:
            print(f"[DEBUG] Executing module command: {module_describe_cmd}")
            print(f"[DEBUG] Return Code: {ret}")

        print(out)

    def get_collection(self, collection="default"):
        """Return the command to restore a collection.

        :param collection: collection name to restore
        :type collection: str

        :return: return the ``module restore`` command with the collection name
        :rtype: str
        """
        # raise error if collection is not a string
        if not isinstance(collection, str):
            raise TypeError(f"Type Error: {collection} is not of type string")

        return f"module restore {collection}"

    def test_collection(self, collection="default"):
        """Test the module collection by running ``module restore <collection>``.
        :param collection: collection name to test
        :type collection: str

        :return: return code of ``module restore`` against the collection name
        :rtype: int
        """
        # raise error if collection is not a string
        if not isinstance(collection, str):
            raise TypeError(f"Type Error: {collection} is not of type string")

        module_restore_cmd = f"module restore {collection}"
        cmd = BuildTestCommand()
        cmd.execute(module_restore_cmd)
        ret = cmd.returnCode()

        # print executed command for debugging
        if self.debug:
            print(f"[DEBUG] Executing command: {module_restore_cmd}")
            print(f"[DEBUG] Return Code: {ret}")

        return ret
