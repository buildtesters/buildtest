import logging
import re

from buildtest.defaults import console
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import (
    is_dir,
    is_file,
    is_symlink,
    read_file,
    resolve_path,
    search_files,
    walk_tree,
)

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

    # returncode can be an integer or list of integers
    buildspec_returncode = builder.status["returncode"]

    # if buildspec returncode field is integer we convert to list for check
    if isinstance(buildspec_returncode, int):
        buildspec_returncode = [buildspec_returncode]

    logger.debug("Conducting Return Code check")
    logger.debug(
        "Status Return Code: %s   Result Return Code: %s"
        % (buildspec_returncode, builder.metadata["result"]["returncode"])
    )
    # checks if test returncode matches returncode specified in Buildspec and assign boolean to returncode_match
    returncode_match = builder.metadata["result"]["returncode"] in buildspec_returncode
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


def file_regex_check(builder):
    """This method will check if file exists and conduct a regular expression check using
    `re.search <https://docs.python.org/3/library/re.html#re.search>`_ method. This method is invoked if ``file_regex`` is defined in ``status`` field.
    If file doesn't exist we return False. If file exists we read the file and apply regular expression for every file specified in ``file_regex`` field.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: Returns True if there is a regex match otherwise returns False.
    """

    assert_file_regex = []

    for file_check in builder.status["file_regex"]:
        fname = file_check["file"]
        resolved_fname = resolve_path(fname)
        if not resolved_fname:
            msg = f"[blue]{builder}[/]: Unable to resolve file path: {fname}"
            logger.error(msg)
            console.print(msg, style="red")
            assert_file_regex.append(False)
            continue

        if not is_file(resolved_fname):
            msg = f"[blue]{builder}[/]: File: {resolved_fname} is not a file"
            logger.error(msg)
            console.print(msg, style="red")
            assert_file_regex.append(False)
            continue

        # read file and apply regex
        content = read_file(resolved_fname)
        regex = re.search(file_check["exp"], content)
        console.print(
            f"[blue]{builder}[/]: Performing regex expression '{file_check['exp']}' on file {resolved_fname}"
        )

        if not regex:
            msg = f"[blue]{builder}[/]: Regular expression: '{file_check['exp']}' is not found in file: {resolved_fname}"
            logger.error(msg)
            console.print(msg, style="red")
            assert_file_regex.append(False)
            continue

        assert_file_regex.append(True)

        console.print(
            f"[blue]{builder}[/]: [green]Regular expression on file {resolved_fname} is a MATCH![/green]"
        )

    return all(assert_file_regex)


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


def comparison_check(builder, comparison_type):
    """Perform check on comparison operators (>, >=, <, <=, ==, !=).  The return is a boolean value that determines if the check has passed.
    One can specify multiple assert checks to check each metric with its reference value. When multiple items are specified, the operation is a logical **AND** by default, unless
    ``mode`` is specified and it is `or`, `OR` then the operation is logical **OR**.


    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
        comparison_type (str): A string value which can be 'ge', 'gt', 'le', 'lt', 'eq', 'ne' that is used to determine which comparison type to perform
    Returns:
        bool: True or False for performance check
    """

    COMPARISON_OPERATIONS = {
        "ge": (lambda x, y: x >= y, ">=", "Greater Equal Check"),
        "gt": (lambda x, y: x > y, ">", "Greater Check"),
        "le": (lambda x, y: x <= y, "<=", "Less Than Equal Check"),
        "lt": (lambda x, y: x < y, "<", "Less Than Check"),
        "eq": (lambda x, y: x == y, "==", "Equality Check"),
        "ne": (lambda x, y: x != y, "!=", "Not Equal Check"),
    }

    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    metric_names = list(builder.metadata["metrics"].keys())

    if comparison_type not in COMPARISON_OPERATIONS:
        raise BuildTestError(
            f"comparison_type: {comparison_type} is not a valid comparison type. Valid comparison types are: {list(COMPARISON_OPERATIONS.keys())}"
        )

    comparison_dict = builder.status[f"assert_{comparison_type}"]
    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in comparison_dict["comparisons"]:
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

        if builder.metrics[name]["type"] == "str" and comparison_type in [
            "ge",
            "gt",
            "le",
            "lt",
        ]:
            msg = f"[blue]{builder}[/]: Unable to convert metric: [red]'{name}'[/red] for comparison. The type must be 'int' or 'float' but recieved [red]{builder.metrics[name]['type']}[/red]. "
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        # convert metric value and reference value to int
        conv_value = convert_metrics(
            metric_value=metric_value, dtype=builder.metrics[name]["type"]
        )
        ref_value = convert_metrics(
            metric_value=ref_value, dtype=builder.metrics[name]["type"]
        )

        # if there is a type mismatch then let's stop now before we do comparison
        if (conv_value is None) or (ref_value is None):
            assert_check.append(False)
            continue

        comparison_op, symbol, log_message = COMPARISON_OPERATIONS[comparison_type]
        bool_check = comparison_op(conv_value, ref_value)
        console.print(
            f"[blue]{builder}[/]: testing metric: {name} if {conv_value} {symbol} {ref_value} - Check: {bool_check}"
        )
        assert_check.append(bool_check)

    # perform logical OR if mode is set to 'or' or 'OR' otherwise do logical AND
    if comparison_dict.get("mode") in ["or", "OR"]:
        bool_check = any(assert_check)
    else:
        bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: {log_message}: {bool_check}")

    return bool_check


def contains_check(builder, comparison_type):
    """This method perform check for existence of value in a list of reference values. The ``contains``
    or ``not_contains`` property is used to determine if metric value exist in the reference values.

    The list of assertion is logically **AND** by default, but if ``mode`` is specified then we will perform a logical **OR**.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``contains``
    """
    # a list containing booleans to evaluate reference check for each metric
    assert_check = []
    metric_names = list(builder.metadata["metrics"].keys())

    CONTAINS_OPERATIONS = {
        "contains": (lambda x, y: x in y, "in", "Contains Check"),
        "not_contains": (lambda x, y: x not in y, "not in", "Not Contains Check"),
    }

    if comparison_type not in CONTAINS_OPERATIONS:
        raise BuildTestError(
            f"comparison_type: {comparison_type} is not a valid comparison type. Valid comparison types are: {list(CONTAINS_OPERATIONS.keys())}"
        )

    comparison_dict = builder.status[comparison_type]

    for metric in comparison_dict["comparisons"]:
        name = metric["name"]
        ref_value = metric["ref"]

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
            metric_value=metric_value, dtype=builder.metrics[name]["type"]
        )

        if (conv_value is None) or (ref_value is None):
            console.print(
                f"[blue]{builder}[/]: Skipping metrics check {name} since value is undefined"
            )
            assert_check.append(False)
            continue

        contains_op, sign, log_message = CONTAINS_OPERATIONS[comparison_type]
        bool_check = contains_op(conv_value, ref_value)

        assert_check.append(bool_check)

        console.print(
            f"[blue]{builder}[/]: testing metric: [red]{name}[/red] if [yellow]{conv_value}[/yellow] {sign} [yellow]{ref_value}[/yellow] - Check: {bool_check}"
        )

    if comparison_dict.get("mode") in ["or", "OR"]:
        bool_check = any(assert_check)
    else:
        bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: {log_message}: {bool_check}")

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
    range_comparisons = builder.status["assert_range"]
    # iterate over each metric in buildspec and determine reference check for each metric
    for metric in range_comparisons["comparisons"]:
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

        metric_type = builder.metrics[name]["type"]

        if builder.metrics[name]["type"] == "str":
            msg = f"[blue]{builder}[/]: Unable to convert metric: [red]'{name}'[/red] for comparison. The type must be 'int' or 'float' but recieved [red]{metric_type}[/red]. "
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        conv_value = convert_metrics(metric_value, dtype=metric_type)
        lower_bound = convert_metrics(lower_bound, dtype=metric_type)
        upper_bound = convert_metrics(upper_bound, dtype=metric_type)

        # if any item is None we stop before we run comparison
        if any(item is None for item in [conv_value, lower_bound, upper_bound]):
            assert_check.append(False)
            continue

        bool_check = lower_bound <= conv_value <= upper_bound
        assert_check.append(bool_check)
        console.print(
            f"[blue]{builder}[/]: testing metric: {name} if {lower_bound} <= {conv_value} <= {upper_bound} - Check: {bool_check}"
        )

    mode = range_comparisons.get("mode")
    # perform logical OR if mode is set to 'or' or 'OR' otherwise do logical AND
    range_check = any(assert_check) if mode in ["or", "OR"] else all(assert_check)

    console.print(f"[blue]{builder}[/]: Range Check: {range_check}")
    return range_check


def file_count_check(builder):
    """This method is used to perform file count check when ``file_count`` property is specified
    in status check. This method will evaluate the number of files in a directory and compare it
    with the reference specified via ``count``. The comparison is done using ``==`` operator.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name

    Returns:
        bool: True or False for performance check ``file_count``
    """
    # a list containing booleans to evaluate reference check for each metric
    assert_check = []

    # iterate over each metric in buildspec and determine reference check for each metric
    for dir_check in builder.status["file_count"]:
        if not is_dir(dir_check["dir"]):
            msg = f"[blue]{builder}[/]: Unable to find directory: [red]{dir_check['dir']}[/red]."
            console.print(msg)
            logger.warning(msg)
            assert_check.append(False)
            continue

        files_by_directory_walk = []
        files_by_regex = []

        # need to walk directory tree if 'ext' attribute is specified or 'filepattern' attribute is not specified.
        if dir_check.get("ext") or not dir_check.get("filepattern"):
            files_by_directory_walk = walk_tree(
                dir_check["dir"],
                ext=dir_check.get("ext"),
                max_depth=dir_check.get("depth"),
                file_type=dir_check.get("filetype"),
                file_traverse_limit=dir_check.get("file_traverse_limit"),
            )
        # if 'filepattern' attribute is specified we will search for files via search_files method which will perform directory traversal based on regular expression
        if dir_check.get("filepattern"):
            files_by_regex = search_files(
                dir_check["dir"],
                regex_pattern=dir_check["filepattern"],
                max_depth=dir_check.get("depth"),
                file_type=dir_check.get("filetype"),
                file_traverse_limit=dir_check.get("file_traverse_limit"),
            )

        total_files = list(set(files_by_directory_walk + files_by_regex))
        bool_check = len(total_files) == dir_check["count"]
        assert_check.append(bool_check)

        # need to get a resolved path for printing purposes. User can specify arbitrary directory name it may not exist on filesystem
        resolved_dirname = resolve_path(dir_check["dir"], exist=False)
        logger.debug(
            f"[blue]{builder}[/]: Found the following files: {total_files} in directory: {resolved_dirname}"
        )

        console.print(
            f"[blue]{builder}[/]: Found {len(total_files)} file in directory: {resolved_dirname}. Comparing with reference count: {dir_check['count']}. Comparison check is {len(total_files)} == {dir_check['count']} which evaluates to {bool_check}"
        )

    # perform a logical AND on the list and return the boolean result
    bool_check = all(assert_check)

    console.print(f"[blue]{builder}[/]: File Count Check: {bool_check}")
    return bool_check
