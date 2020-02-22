import os
import sys

sys.path.insert(0, os.getenv("BUILDTEST_ROOT"))

from buildtest.modules.util import get_all_collections, ModuleCollection

collections = get_all_collections()
collections += ["invalid_collection"]
for i in collections:
    collection_object = ModuleCollection(i)
    print(collection_object.get_command())
    ec = collection_object.test_collection()
    if ec != 0:
        print(f"Failed to load collection: {i} with exit status: {ec}")
    else:
        print(f"Successfully loaded collection: {i}")
