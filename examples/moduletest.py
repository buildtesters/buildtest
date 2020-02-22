import os
import sys

sys.path.insert(0, os.getenv("BUILDTEST_ROOT"))

from buildtest.modules.util import Module

mod_names = ["GCCcore", "Python"]

a = Module(mod_names)
module_cmds = a.get_command()
rc = a.test_modules()

if rc == 0:
    print (f"The following modules:  {mod_names} were loaded successfully")
    print ("\n")
    print ("Command Executed:")
    print("----------------------------")
    print (module_cmds)

bad_names = ["GCCcore", "invalid"]
b = Module(bad_names)

print (f"Failed to load modules: {bad_names}, return code: {b.test_modules()}, Command Executed: {b.get_command()} ")
