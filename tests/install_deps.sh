# Original Script is found in easybuilders/easybuild-framework:  https://github.com/easybuilders/easybuild-framework/blob/develop/easybuild/scripts/install_eb_dep.sh
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
export MOD_INIT=$PREFIX/lmod/$VERSION/init/bash

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