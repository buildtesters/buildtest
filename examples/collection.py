from buildtest.module import get_all_collections, Module

collections = get_all_collections()

for i in collections:
    a = Module()
    restore_cmd, ret_code = a.get_collection(i), a.test_collection(i)

    print(f"Collection Command: {restore_cmd}    Return Code: {ret_code}")

# test Python collection with debug enabled
a = Module(debug=True)
a.test_collection("Python")

# test default collection with debug enabled
a = Module(debug=True)
a.test_collection()

# This will raise an exception
a.test_collection(1)
