#!/usr/bin/env python3

# This run_tests.sh file is intended to invoke python testing of buildtest.
# It is required that buildtest is installed, or interacted with 
# from the root of the development directory.


# Run tests just for everything else
pytest -vra tests/
