from setup import *
from process_easyconfig import *

module="GCC"
version="5.4.0-2.27"

print module, version
print BUILDTEST_ROOT, BUILDTEST_SRCDIR, BUILDTEST_EASYCONFIGDIR

moduleversion_dict=module_version_relation(BUILDTEST_MODULEROOT)
print_module_version(moduleversion_dict)

print "----------------"
moduleversion_toolchain_relation(BUILDTEST_MODULEROOT)

