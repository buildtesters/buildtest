#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    exit 1
fi
VERSION=$1
LMOD_PACKAGE=Lmod-$VERSION
PREFIX=/opt/apps

PKG_URL="https://github.com/TACC/Lmod/archive/${VERSION}.tar.gz"
export PATH=$PREFIX/lmod/$VERSION/libexec:$PATH
export MOD_INIT=$HOME/lmod/$VERSION/init/bash

echo "Installing ${LMOD_PACKAGE} @ ${PREFIX}..."
mkdir -p ${PREFIX}
set +e
wget ${PKG_URL} && tar xfz *${VERSION}.tar.gz
set -e
cd $LMOD_PACKAGE
./configure --prefix=$PREFIX && make && make install

if [ ! -z $MOD_INIT ]; then
        source $MOD_INIT
        type module
fi