#!/usr/bin/env python3

# This run_tests.sh file is intended to invoke python testing of buildtest.
# It is required that buildtest is installed, or interacted with 
# from the root of the development directory.

if [[ -z "$LMOD_DIR" ]] && [[ -d "${LMOD_DIR}" ]]; then
    printf "Lmod directory found on path, running module tests\n"
    pytest -vra tests/test_modules.py
fi

# Run tests just for everything else
pytest -vra tests/test_config_file.py tests/test_file.py tests/test_inspect.py
