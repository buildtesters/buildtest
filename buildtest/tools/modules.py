def get_module_commands(modules):
    """Return a list of module command as a list of instructions based on
    ``module`` property which can be defined in the configuration or compiler schema

     Args:
        modules (dict): The module property specified in buildspec or configuration file

     Returns:
        list: a list of module commands
    """

    if not modules or not isinstance(modules, dict):
        return

    module_cmd = []

    # if purge is True and defined add module purge
    if modules.get("purge"):
        module_cmd += ["module purge"]

    if modules.get("restore"):
        module_cmd += [f"module restore {modules['restore']}"]

    if modules.get("swap"):
        module_cmd += [f"module swap {' '.join(modules['swap'])}"]

    if modules.get("load"):
        for name in modules["load"]:
            module_cmd += [f"module load {name}"]

    return module_cmd
