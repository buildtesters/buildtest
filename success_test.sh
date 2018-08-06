buildtest -s GCC/5.4.0-2.27 --shell csh
_buildtest --system all
_buildtest --system gcc
_buildtest -s intel/2017.01 
_buildtest -s Python/2.7.14-intel-2018a --python-package dateutil
_buildtest -s R/3.4.3-intel-2018a-X11-20171023 --r-package abc
_buildtest -s Ruby/2.5.0-intel-2018a --ruby-package addressable
 _buildtest -s Perl/5.26.0-GCCcore-6.4.0 --perl-package AnyData
_buildtest -s Tcl/.8.6.5 -t intel/2017.01


