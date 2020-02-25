import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from buildtest.modules.spider import Spider
from buildtest.modules.util import Module

a = Spider()
names = a.get_unique_software()
print(f"Module Trees: {a.get_trees()}")
print("{:_<80}".format(""))
print(f"Unique Software: {names}")

print("\n")

parents = a.get_all_parents()
print(f"Parent Modules: {parents}")

print("\n")

gcc_versions = a.get_all_versions("GCC")
print(f"GCC Versions: {gcc_versions}")

print("\n")

b = Spider("/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core")
mod_names = b.get_modules()
print(f"Module Trees: {b.get_trees()}")
print(f"Unique Software: {b.get_unique_software()}")
print(f"Module Names: {mod_names}")

# testing all modules
for x in mod_names:
    cmd = Module(x, debug=True)
    cmd.test_modules()
