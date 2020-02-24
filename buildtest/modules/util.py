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


class ModuleCollection:
    """Class declaration of ModuleCollection."""

    def __init__(self, collection):
        """Initializer method of ModuleCollection class.

        :param collection: name of module collection
        :type collection: str
        """

        # raise TypeError exception if collection is not a string type since that is required
        # when working with module collection
        if not isinstance(collection, str):
            raise TypeError(f"Type Error: {collection} is not of type string")

        self.collection = collection
        self.module_cmd = f"module restore {self.collection}"

    def test_collection(self):
        """Test the module collection by running ``module restore <collection>``.

        :return: return code of ``module restore`` command
        :rtype: int
        """

        cmd = BuildTestCommand()
        cmd.execute(self.module_cmd)
        return cmd.returnCode()

    def get_command(self):
        """ Get the module command used to restore a collection

        :return: Return the actual command to restore a collection.
        :rtype: str
        """

        return self.module_cmd


class Module:
    """Class declaration for Module class"""

    def __init__(self, modules, purge=True, force=False):
        """Initialize method for Module class.

        :param modules: list of modules
        :param purge: boolean to control whether to purge modules before loading
        :param force: boolean to control whether to force purge modules before loading

        :type modules: list
        :type purge: bool
        :type force: bool
        """

        # raise TypeError exception if collection is not a string type since that is required
        # when working with module collection
        if not isinstance(modules, list):
            raise TypeError(f"Type Error: {collection} is not of type list")

        self.modules = modules
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
        cmd = BuildTestCommand()
        cmd.execute(self.module_load_cmd)
        return cmd.returnCode()

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

        # For some odd reason, the output of module save gets passed to STDERR stream instead of STDOUT.
        out = cmd.get_error()

        print(out)
