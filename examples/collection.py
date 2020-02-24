import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from buildtest.modules.util import get_all_collections, ModuleCollection

collections = get_all_collections()

# adding a collection name "invalid_collection" that is bound to fail
collections = collections + ["invalid_collection"]
for i in collections:
    collection_object = ModuleCollection(i)
    print(collection_object.get_command())
    ec = collection_object.test_collection()
    if ec != 0:
        print(f"Failed to load collection: {i} with exit status: {ec}")
    else:
        print(f"Successfully loaded collection: {i}")

# test Python collection with debug enabled
a = ModuleCollection("Python", debug=True)
a.test_collection()

# Type Error when passing a collection name not of string type
ModuleCollection(1)
