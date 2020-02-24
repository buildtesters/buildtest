import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from buildtest.modules.util import Module

a = Module("zlib", debug=True)
# save module collection with name "zlib"
a.save("zlib")
# show module collection "zlib"
a.describe("zlib")
# show "default" module collection
a.describe()

# Passing a list will throw a type error. since collection name must be a string
a.describe(["zlib"])
