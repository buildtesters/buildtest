#!/bin/bash

_buildtest build --system gcc
_buildtest build -s GCCcore/6.4.0
_buildtest build -s GCCcore/6.4.0 --shell csh
_buildtest build -s GCCcore/6.4.0 --enable-job

_buildtest build -s Python/2.7.14-intel-2018a --python-package dateutil
_buildtest build -s R/3.4.3-intel-2018a-X11-20171023 --r-package abc
_buildtest build -s Ruby/2.5.0-intel-2018a --ruby-package addressable
_buildtest build -s Perl/5.26.0-GCCcore-6.4.0 --perl-package AnyData


