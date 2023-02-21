import logging
import re

from buildtest.defaults import console
from buildtest.utils.file import is_dir, is_file, is_symlink, resolve_path

logger = logging.getLogger(__name__)


def is_metrics_defined(builder, name):
    """Returns True if metrics value is defined, otherwise returns False

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
        name (str): Name of metric

    """
    if builder.metadata["metrics"][name] == "":
        msg = f"[blue]{builder}[/]: Skipping metrics check for [blue]{name}[/blue] since value is undefined"
        console.print(msg)
        logger.warning(msg)
        return False

    return True


def returncode_check(builder):
    """Check status check of ``returncode`` field if specified in status property.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
    """

    returncode_match = False

    # if 'returncode' field set for 'status' check the returncode if its not set we return False
    if "returncode" in builder.status.keys():
        # returncode can be an integer or list of integers
        buildspec_returncode = builder.status["returncode"]

        # if buildspec returncode field is integer we convert to list for check
        if isinstance(buildspec_returncode, int):
            buildspec_returncode = [buildspec_returncode]

        logger.debug("Conducting Return Code check")
        logger.debug(
            "Status Return Code: %s   Result Return Code: %s"
            % (
                buildspec_returncode,
                builder.metadata["result"]["returncode"],
            )
        )
        # checks if test returncode matches returncode specified in Buildspec and assign boolean to returncode_match
        returncode_match = (
            builder.metadata["result"]["returncode"] in buildspec_returncode
        )
        console.print(
            f"[blue]{builder}[/]: Checking returncode - {builder.metadata['result']['returncode']} is matched in list {buildspec_returncode}"
        )

    return returncode_match


def runtime_check(builder):
    """This method will return a boolean (True/False) based on runtime specified in buildspec and check with test runtime.
    User can specify both `min` and `max`, or just specify `min` or `max`.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
    """

    if not builder.status.get("runtime"):
        return False

    min_time = builder.status["runtime"].get("min") or 0
    max_time = builder.status["runtime"].get("max")

    actual_runtime = builder.get_runtime()

    # if min specified
    if min_time and not max_time:
        console.print(
            f"[blue]{builder}[/]: Checking  mintime < runtime: {float(min_time)} < {actual_runtime}"
        )
        return float(min_time) < actual_runtime

    # if max specified
    if not min_time and max_time:
        console.print(
            f"[blue]{builder}[/]: Checking runtime < maxtime: {actual_runtime} < {float(max_time)} "
        )
        return actual_runtime < float(max_time)

    # if both min and max are specified
    console.print(
        f"[blue]{builder}[/]: Checking mintime < runtime < maxtime: {float(min_time)} < {actual_runtime} < {float(max_time)} "
    )
    return float(min_time) < actual_runtime < float(max_time)


def regex_check(builder):
    """This method conducts a regular expression check using
    `re.search <https://docs.python.org/3/library/re.html#re.search>`_
    with regular expression defined in Buildspec. User must specify an
    output stream (stdout, stderr) to select when performing regex. In
    buildtest, this would read the .out or .err file based on stream and
    run the regular expression to see if there is a match. This method
    will return a boolean True indicates there is a match otherwise False
    if ``regex`` object not defined or ``re.search`` doesn't find a match.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: Returns True if their is a regex match otherwise returns False.
    """

    if not builder.status.get("regex"):
        return False

    file_stream = None
    if builder.status["regex"]["stream"] == "stdout":
        logger.debug(
            f"Detected regex stream 'stdout' so reading output file: {builder.metadata['outfile']}"
        )
        content = builder.output()

        file_stream = builder.metadata["outfile"]

    elif builder.status["regex"]["stream"] == "stderr":
        logger.debug(
            f"Detected regex stream 'stderr' so reading error file: {builder.metadata['errfile']}"
        )
        content = builder.error()

        file_stream = builder.metadata["errfile"]

    logger.debug(f"Applying re.search with exp: {builder.status['regex']['exp']}")

    regex = re.search(builder.status["regex"]["exp"], content)

    console.print(
        f"[blue]{builder}[/]: performing regular expression - '{builder.status['regex']['exp']}' on file: {file_stream}"
    )
    if not regex:
        console.print(f"[blue]{builder}[/]: Regular Expression Match - [red]Failed![/]")
        return False

    console.print(f"[blue]{builder}[/]: Regular Expression Match - [green]Success![/]")

    return True


def is_symlink_check(builder):
    """This method will perform symlink status check for ``is_symlink`` property. Each item is tested for symblolic link
    and returns a boolean to inform if all items are symbolic links or not.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
    Returns:
        bool: A boolean for is_symlink status check
    """
    assert_exists = []
    console.print(
        f"[blue]{builder}[/]: Check all items:  {builder.status['is_symlink']}  for symbolic links"
    )
    for filename in builder.status["is_symlink"]:

        if is_symlink(filename):
            console.print(
                f"[blue]{builder}[/]: {filename} is a symbolic link to {resolve_path(filename)}"
            )
            assert_exists.append(True)
        else:
            console.print(
                f"[blue]{builder}[/]: {filename} is broken or not a symbolic link"
            )
            assert_exists.append(False)

    bool_check = all(assert_exists)
    console.print(f"[blue]{builder}[/]: Symlink Check: {bool_check}")
    return bool_check


def exists_check(builder):
    """This method will perform status check for ``exists`` property. Each value is tested for file
    existence and returns a boolean to inform if all files exist or not.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
    Returns:
        bool: A boolean for exists status check
    """
    assert_exists = all(
        resolve_path(file, exist=True) for file in builder.status["exists"]
    )
    console.print(
        f"[blue]{builder}[/]: Test all files:  {builder.status['exists']}  existences "
    )
    for fname in builder.status["exists"]:
        resolved_fname = resolve_path(fname)
        if resolved_fname:
            console.print(f"[blue]{builder}[/]: file: {resolved_fname} exists")
        else:
            console.print(f"[blue]{builder}[/]: file: {fname} does not exist")

    console.print(f"[blue]{builder}[/]: Exist Check: {assert_exists}")
    return assert_exists


def is_file_check(builder):
    """This method will perform status check for ``is_file`` property. Each item in ``is_file`` is
     checked by determining if its a file. The return is a single boolean where we perform a logical AND
     to determine final status check for is_file

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
    Returns:
        bool: A boolean for is_file status check
    """

    assert_is_file = all(is_file(file) for file in builder.status["is_file"])
    console.print(
        f"[builder]{builder}[/]: Test all files:  {builder.status['is_file']}  existences "
    )
    for fname in builder.status["is_file"]:
        resolved_fname = resolve_path(fname, exist=True)
        if is_file(resolved_fname):
            console.print(f"[blue]{builder}[/]: file: {resolved_fname} is a file ")
        else:
            console.print(f"[blue]{builder}[/]: file: {fname} is not a file")

    console.print(f"[blue]{builder}[/]: File Existence Check: {assert_is_file}")
    return assert_is_file


def is_dir_check(builder):
    """This method will perform status check for ``is_dir`` property. Each item in ``is_dir`` is
     checked by determining if its a directory. The return is a single boolean where we perform a logical AND
     to determine final status check for ``is_dir``

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
    Returns:
        bool: A boolean for ``is_dir`` status check
    """

    assert_is_dir = all(is_dir(file) for file in builder.status["is_dir"])
    console.print(
        f"[blue]{builder}[/]: Test all files:  {builder.status['is_dir']}  existences "
    )
    for dirname in builder.status["is_dir"]:
        resolved_dirname = resolve_path(dirname)
        if is_dir(resolved_dirname):
            console.print(
                f"[blue]{builder}[/]: file: {resolved_dirname} is a directory "
            )
        else:
            console.print(f"[blue]{builder}[/]: file: {dirname} is not a directory")

    console.print(f"[blue]{builder}[/]: Directory Existence Check: {assert_is_dir}")
    return assert_is_dir


def convert_metrics(metric_value, dtype):
    """This method will convert input argument ``metric_value`` and ``ref_value`` to the datatype defined
    by ``dtype`` which can be **int**, **float**, or **str**

    Args:
        metric_value: Value assigned to metric that is converted to its type defined by dtype
        dtype (str): A string value which can be 'str', 'int', 'float'

    Returns:
        Tuple: A tuple consisting of (metric_value, ref_value)
    """
    conv_metric_val = None

    if dtype == "int":
        # the metric_value is a string therefore to convert to int, one must convert to float before converting to int
        try:
            conv_metric_val = int(float(metric_value))
        except ValueError:
            console.print_exception(show_locals=True)
    elif dtype == "float":
        try:
            conv_metric_val = float(metric_value)
        except ValueError:
            console.print_exception(show_locals=True)
    elif dtype == "str":
        try:
            conv_metric_val = str(metric_value)
        except ValueError:
            console.print_exception(show_locals=True)

    return conv_metric_val


def assert_ge_check(builder):
    """Perform check on assert greater and equal when ``assert_ge`` is specified in buildspec. The return is a boolean value that determines if the check has passed.
    One can specify multiple assert checks to check each metric with its reference value. When multiple items are specified, the operation is a logical AND and all checks
    must be ``True``.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``assert_ge``
    """

    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in builder.status["assert_ge"]:
        name = metric["name"]
        ref_value = metric["ref"]

        # if metric is not valid, then mark as False
        if not builder.is_valid_metric(name):
            msg = f"[blue]{builder}[/]: Unable to find metric: [red]{name}[/red]. List of valid metrics are the following: {metric_names}"
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        metric_value = builder.metadata["metrics"][name]

        if not is_metrics_defined(builder, name):
            assert_check.append(False)
            continue

        if builder.metrics[name]["type"] == "str":
            msg = f"[blue]{builder}[/]: Unable to convert metric: [red]'{name}'[/red] for comparison. The type must be 'int' or 'float' but recieved [red]{builder.metrics[name]['type']}[/red]. "
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        # convert metric value and reference value to int
        conv_value = convert_metrics(
            metric_value=metric_value,
            dtype=builder.metrics[name]["type"],
        )
        ref_value = convert_metrics(
            metric_value=ref_value,
            dtype=builder.metrics[name]["type"],
        )

        # if there is a type mismatch then let's stop now before we do comparison
        if (conv_value is None) or (ref_value is None):
            assert_check.append(False)
            continue

        bool_check = conv_value >= ref_value
        console.print(
            f"[blue]{builder}[/]: testing metric: {name} if {conv_value} >= {ref_value} - Check: {bool_check}"
        )
        assert_check.append(bool_check)

    # perform a logical AND on the list and return the boolean result
    bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: Greater Equal Check: {bool_check}")
    return bool_check


def assert_le_check(builder):
    """Perform check on assert less than and equal when ``assert_le`` is specified in buildspec. The return is a boolean value that determines if the check has passed.
    One can specify multiple assert checks to check each metric with its reference value. When multiple items are specified, the operation is a logical AND and all checks
    must be ``True``.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``assert_le``
    """

    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in builder.status["assert_le"]:
        name = metric["name"]
        ref_value = metric["ref"]

        # if metric is not valid, then mark as False
        if not builder.is_valid_metric(name):
            msg = f"[blue]{builder}[/]: Unable to find metric: [red]{name}[/red]. List of valid metrics are the following: {metric_names}"
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        metric_value = builder.metadata["metrics"][name]

        if not is_metrics_defined(builder, name):
            assert_check.append(False)
            continue

        if builder.metrics[name]["type"] == "str":
            msg = f"[blue]{builder}[/]: Unable to convert metric: [red]'{name}'[/red] for comparison. The type must be 'int' or 'float' but recieved [red]{builder.metrics[name]['type']}[/red]. "
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        # convert metric value and reference value to int
        conv_value = convert_metrics(
            metric_value=metric_value,
            dtype=builder.metrics[name]["type"],
        )
        ref_value = convert_metrics(
            metric_value=ref_value,
            dtype=builder.metrics[name]["type"],
        )

        # if there is a type mismatch then let's stop now before we do comparison
        if (conv_value is None) or (ref_value is None):
            assert_check.append(False)
            continue

        bool_check = conv_value <= ref_value
        console.print(
            f"[blue]{builder}[/]: testing metric: {name} if {conv_value} <= {ref_value} - Check: {bool_check}"
        )
        assert_check.append(bool_check)

    # perform a logical AND on the list and return the boolean result
    bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: Less Than Equal Check: {bool_check}")
    return bool_check


def assert_gt_check(builder):
    """Perform check on assert greater than when ``assert_gt`` is specified in buildspec. The return is a boolean value that determines if the check has passed.
    One can specify multiple assert checks to check each metric with its reference value. When multiple items are specified, the operation is a logical AND and all checks
    must be ``True``.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``assert_gt``
    """

    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in builder.status["assert_gt"]:
        name = metric["name"]
        ref_value = metric["ref"]

        # if metric is not valid, then mark as False
        if not builder.is_valid_metric(name):
            msg = f"[blue]{builder}[/]: Unable to find metric: [red]{name}[/red]. List of valid metrics are the following: {metric_names}"
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        metric_value = builder.metadata["metrics"][name]

        if not is_metrics_defined(builder, name):
            assert_check.append(False)
            continue

        if builder.metrics[name]["type"] == "str":
            msg = f"[blue]{builder}[/]: Unable to convert metric: [red]'{name}'[/red] for comparison. The type must be 'int' or 'float' but recieved [red]{builder.metrics[name]['type']}[/red]. "
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        # convert metric value and reference value to int
        conv_value = convert_metrics(
            metric_value=metric_value,
            dtype=builder.metrics[name]["type"],
        )
        ref_value = convert_metrics(
            metric_value=ref_value,
            dtype=builder.metrics[name]["type"],
        )

        # if there is a type mismatch then let's stop now before we do comparison
        if (conv_value is None) or (ref_value is None):
            assert_check.append(False)
            continue

        bool_check = conv_value > ref_value
        console.print(
            f"[blue]{builder}[/]: testing metric: {name} if {conv_value} > {ref_value} - Check: {bool_check}"
        )
        assert_check.append(bool_check)

    # perform a logical AND on the list and return the boolean result
    bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: Greater Check: {bool_check}")
    return bool_check


def assert_lt_check(builder):
    """Perform check on assert less than when ``assert_lt`` is specified in buildspec. The return is a boolean value that determines if the check has passed.
    One can specify multiple assert checks to check each metric with its reference value. When multiple items are specified, the operation is a logical AND and all checks
    must be ``True``.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``assert_lt``
    """

    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in builder.status["assert_lt"]:
        name = metric["name"]
        ref_value = metric["ref"]

        # if metric is not valid, then mark as False
        if not builder.is_valid_metric(name):
            msg = f"[blue]{builder}[/]: Unable to find metric: [red]{name}[/red]. List of valid metrics are the following: {metric_names}"
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        metric_value = builder.metadata["metrics"][name]

        if not is_metrics_defined(builder, name):
            assert_check.append(False)
            continue

        if builder.metrics[name]["type"] == "str":
            msg = f"[blue]{builder}[/]: Unable to convert metric: [red]'{name}'[/red] for comparison. The type must be 'int' or 'float' but recieved [red]{builder.metrics[name]['type']}[/red]. "
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        # convert metric value and reference value to int
        conv_value = convert_metrics(
            metric_value=metric_value,
            dtype=builder.metrics[name]["type"],
        )
        ref_value = convert_metrics(
            metric_value=ref_value,
            dtype=builder.metrics[name]["type"],
        )

        # if there is a type mismatch then let's stop now before we do comparison
        if (conv_value is None) or (ref_value is None):
            assert_check.append(False)
            continue

        bool_check = conv_value < ref_value
        console.print(
            f"[blue]{builder}[/]: testing metric: {name} if {conv_value} < {ref_value} - Check: {bool_check}"
        )
        assert_check.append(bool_check)

    # perform a logical AND on the list and return the boolean result
    bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: Less Than Check: {bool_check}")
    return bool_check


def assert_eq_check(builder):
    """This method is perform Assert Equality used when ``assert_eq`` property is specified
    in status check. This method will evaluate each metric value reference value and
    store assertion in list. The list of assertion is logically AND which will return a True or False
    for the status check.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``assert_eq``
    """
    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in builder.status["assert_eq"]:
        name = metric["name"]
        ref_value = metric["ref"]

        # if metric is not valid, then mark as False
        if not builder.is_valid_metric(name):
            msg = f"[blue]{builder}[/]: Unable to find metric: [red]{name}[/red]. List of valid metrics are the following: {metric_names}"
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        metric_value = builder.metadata["metrics"][name]

        if not is_metrics_defined(builder, name):
            assert_check.append(False)
            continue

        conv_value = convert_metrics(
            metric_value=metric_value,
            dtype=builder.metrics[name]["type"],
        )
        ref_value = convert_metrics(
            metric_value=ref_value,
            dtype=builder.metrics[name]["type"],
        )

        # if either converted value and reference value is None stop here before proceeding to equality check
        if (conv_value is None) or (ref_value is None):
            assert_check.append(False)
            continue

        bool_check = conv_value == ref_value
        console.print(
            f"[blue]{builder}[/]: testing metric: {name} if {conv_value} == {ref_value} - Check: {bool_check}"
        )
        assert_check.append(bool_check)

    # perform a logical AND on the list and return the boolean result
    bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: Equality Check: {bool_check}")
    return bool_check


def assert_ne_check(builder):
    """This method performs Assert not Equal and is used when ``assert_ne`` property is specified
    in status check. This method will evaluate each metric value reference value and
    store assertion in list. The list of assertion is logically AND which will return a True or False
    for the status check.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``assert_ne``
    """
    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in builder.status["assert_ne"]:
        name = metric["name"]
        ref_value = metric["ref"]

        # if metric is not valid, then mark as False
        if not builder.is_valid_metric(name):
            msg = f"[blue]{builder}[/]: Unable to find metric: [red]{name}[/red]. List of valid metrics are the following: {metric_names}"
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        metric_value = builder.metadata["metrics"][name]

        if not is_metrics_defined(builder, name):
            assert_check.append(False)
            continue

        conv_value = convert_metrics(
            metric_value=metric_value,
            dtype=builder.metrics[name]["type"],
        )
        ref_value = convert_metrics(
            metric_value=ref_value,
            dtype=builder.metrics[name]["type"],
        )

        # if either converted value and reference value is None stop here before proceeding to the not equal check
        if (conv_value is None) or (ref_value is None):
            assert_check.append(False)
            continue

        bool_check = conv_value != ref_value
        console.print(
            f"[blue]{builder}[/]: testing metric: {name} if {conv_value} != {ref_value} - Check: {bool_check}"
        )
        assert_check.append(bool_check)

    # perform a logical AND on the list and return the boolean result
    bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: Not Equal Check: {bool_check}")
    return bool_check


def contains_check(builder):
    """This method perform Contains check when ``contains`` property is specified
    in status check. This method will each metric value is in list of reference values.
    The list of assertion is logically AND which will return a True or False
    for the status check.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``contains``
    """
    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in builder.status["contains"]:
        name = metric["name"]
        ref_value = metric["ref"]

        # if metric is not valid, then mark as False
        if not builder.is_valid_metric(name):
            msg = f"[blue]{builder}[/]: Unable to find metric: [red]{name}[/red]. List of valid metrics are the following: {metric_names}"
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        metric_value = builder.metadata["metrics"][name]

        if not is_metrics_defined(builder, name):
            assert_check.append(False)
            continue

        conv_value = convert_metrics(
            metric_value=metric_value,
            dtype=builder.metrics[name]["type"],
        )

        # if either converted value and reference value is None stop here before proceeding to the not equal check
        if (conv_value is None) or (ref_value is None):
            console.print(
                f"[blue]{builder}[/]: Skipping metrics check {name} since value is undefined"
            )
            assert_check.append(False)
            continue

        bool_check = conv_value in ref_value
        assert_check.append(bool_check)

        console.print(
            f"[blue]{builder}[/]: testing metric: [red]{name}[/red] if [yellow]{conv_value}[/yellow] in [yellow]{ref_value}[/yellow] - Check: {bool_check}"
        )

    # perform a logical AND on the list and return the boolean result
    bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: Contains Check: {bool_check}")
    return bool_check


def notcontains_check(builder):
    """This method perform Not Contains check when ``not_contains`` property is specified
    in status check. This method will each metric value is in list of reference values.
    The list of assertion is logically AND which will return a True or False
    for the status check.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``not_contains``
    """
    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in builder.status["not_contains"]:
        name = metric["name"]
        ref_value = metric["ref"]

        # if metric is not valid, then mark as False
        if not builder.is_valid_metric(name):
            msg = f"[blue]{builder}[/]: Unable to find metric: [red]{name}[/red]. List of valid metrics are the following: {metric_names}"
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        metric_value = builder.metadata["metrics"][name]

        if not is_metrics_defined(builder, name):
            assert_check.append(False)
            continue

        conv_value = convert_metrics(
            metric_value=metric_value,
            dtype=builder.metrics[name]["type"],
        )

        # if either converted value and reference value is None stop here before proceeding to the not equal check
        if (conv_value is None) or (ref_value is None):
            console.print(
                f"[blue]{builder}[/]: Skipping metrics check {name} since value is undefined"
            )
            assert_check.append(False)
            continue

        bool_check = conv_value not in ref_value
        assert_check.append(bool_check)

        console.print(
            f"[blue]{builder}[/]: testing metric: [red]{name}[/red] if [yellow]{conv_value}[/yellow] not in [yellow]{ref_value}[/yellow] - Check: {bool_check}"
        )

    # perform a logical AND on the list and return the boolean result
    bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: Not Contains Check: {bool_check}")
    return bool_check


def assert_range_check(builder):
    """This method is perform Assert Range used when ``assert_range`` property is specified
    in status check. This method will evaluate each metric value with lower and upper bound and
    store assertion in list. The list of assertion is logically AND which will return a True or False
    for the status check.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``assert_range``
    """

    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in builder.status["assert_range"]:
        name = metric["name"]
        lower_bound = metric["lower"]
        upper_bound = metric["upper"]

        # if metric is not valid, then mark as False
        if not builder.is_valid_metric(name):
            msg = f"[blue]{builder}[/]: Unable to find metric: [red]{name}[/red]. List of valid metrics are the following: {metric_names}"
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        metric_value = builder.metadata["metrics"][name]

        if not is_metrics_defined(builder, name):
            assert_check.append(False)
            continue

        if builder.metrics[name]["type"] == "str":
            msg = f"[blue]{builder}[/]: Unable to convert metric: [red]'{name}'[/red] for comparison. The type must be 'int' or 'float' but recieved [red]{builder.metrics[name]['type']}[/red]. "
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        conv_value = convert_metrics(
            metric_value=metric_value,
            dtype=builder.metrics[name]["type"],
        )
        lower_bound = convert_metrics(
            metric_value=lower_bound,
            dtype=builder.metrics[name]["type"],
        )
        lower_bound = convert_metrics(
            metric_value=lower_bound,
            dtype=builder.metrics[name]["type"],
        )
        upper_bound = convert_metrics(
            metric_value=upper_bound,
            dtype=builder.metrics[name]["type"],
        )

        # if any item is None we stop before we run comparison
        if any(item is None for item in [conv_value, lower_bound, upper_bound]):
            assert_check.append(False)
            continue

        bool_check = lower_bound <= conv_value <= upper_bound
        assert_check.append(bool_check)
        console.print(
            f"[blue]{builder}[/]: testing metric: {name} if {lower_bound} <= {conv_value} <= {upper_bound} - Check: {bool_check}"
        )
    # perform a logical AND on the list and return the boolean result
    range_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: Range Check: {range_check}")
    return range_check
