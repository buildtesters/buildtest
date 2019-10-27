#!/bin/csh

set sourced=($_)
if ("$sourced" != "") then
    set fpath = `realpath -e $sourced[2]`
    set ROOT = `dirname $fpath`
    setenv BUILDTEST_ROOT $ROOT
    set path = ( $path $ROOT)
    cd $BUILDTEST_ROOT
endif
