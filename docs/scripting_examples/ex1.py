import os
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.menu.build import discover_buildspecs

included_bp, excluded_bp = discover_buildspecs(
    buildspec=[os.path.join(BUILDTEST_ROOT, "tutorials")]
)
print(f"discovered_buildspec: {included_bp}   excluded buildspec: {excluded_bp}")
