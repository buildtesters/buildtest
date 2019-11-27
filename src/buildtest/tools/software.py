"""
Application & Toolchain name & version query functions
"""

import os
import stat
from buildtest.tools.modules import module_obj
from buildtest.tools.system import BuildTestCommand


def get_binaries_from_application(module):
    """ return a list of binaries from $PATH variable defined in module file"""

    parent_mod = module_obj.get_parent_modules(module)
    query = ""
    for item in parent_mod:
        query += f"module try-load {item}; "
    cmd = BuildTestCommand()
    query += "$LMOD_CMD bash show " + module
    cmd.execute(query)

    # output of $LMOD_CMD bash show  seems to be backward
    output = cmd.get_error()

    path_str = 'prepend_path("PATH",'

    path_list = []

    for line in output.splitlines():

        if line.find(path_str) != -1:
            # need to extract directory from  a string in the following format
            # prepend_path("PATH","/nfs/grid/software/easybuild/IvyBridge/redhat/7.3/software/GCCcore/6.4.0/bin")

            start_index = line.index(",") + 2
            end_index = line.rfind('"')
            # only add directory if it exists and is part of $PATH variable
            if os.path.exists(line[start_index:end_index]):
                # add directory to list that is being set by PATH variable in module file
                path_list.append(line[start_index:end_index])

    if len(path_list) == 0:
        print(
            "No $PATH set in your module ",
            module,
            "  so no possible binaries can be found",
        )
        return None

    binaries = []

    for dir in path_list:
        # check for files only if directory exists
        for executable in os.listdir(dir):
            executable_filepath = os.path.join(dir, executable)

            # skip loop if it is not a file
            if not os.path.isfile(executable_filepath):
                continue
            # check only files that are executable
            statmode = os.stat(executable_filepath)[stat.ST_MODE] & (
                stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            )

            # skip link files and check if file is executable
            if statmode and not os.path.islink(executable_filepath):
                binaries.append(executable)

    return binaries
