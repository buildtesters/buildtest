from buildtest.menu.inspect import get_all_ids, func_inspect


def test_inspect_ids():

    test_ids = get_all_ids()
    # return should be a list of test ids
    assert isinstance(test_ids, list)
    print(test_ids)

    # check if we have atleast one item and its test id is a string
    assert isinstance(test_ids[0], str) and len(test_ids) > 0

    class args:
        test = test_ids[0]

    func_inspect(args)
