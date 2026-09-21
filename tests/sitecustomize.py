import os

import coverage

config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".coveragerc")
if os.path.exists(config_path):
    coverage.process_startup()
