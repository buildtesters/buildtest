import os
import sys

sys.path.insert(0, os.getenv("BUILDTEST_ROOT"))

from buildtest.modules.util import Module

a = Module(["zlib"])
# save module collection with name "zlib"
a.save("zlib")
# show module collection "zlib"
a.describe("zlib")
# show "default" module collection
a.describe()

# Passing a list will throw a type error. since collection name must be a string
a.describe(["zlib"])
