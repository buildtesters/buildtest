import os
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.menu.build import discover_buildspecs

included_bp, excluded_bp = discover_buildspecs(
    buildspec=[os.path.join(BUILDTEST_ROOT, "tutorials")]
)
print("\n Discovered buildspecs: \n")
[print(f) for f in included_bp]

print("\n Excluded buildspecs: \n")
[print(f) for f in excluded_bp]
