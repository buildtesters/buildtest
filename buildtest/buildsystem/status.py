def get_total_build_ids():
    """Return a total count of build ids. This can be retrieved by getting length
    of "build:" key. Build IDs start from 0.

    :return: return a list of numbers  that represent build id
    :rtype: list
    """

    with open(BUILDTEST_BUILD_LOGFILE, "r") as fd:
        content = json.load(fd)

    total_records = len(content["build"])
    return total_records
