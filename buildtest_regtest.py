import pytest
from buildtest.tools.system import BuildTestSystem

system = BuildTestSystem()
system.check_system_requirements()
pytest.main()