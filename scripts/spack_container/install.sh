git clone https://github.com/spack/spack ~/spack
cd ~/spack
git checkout releases/v0.16
. share/spack/setup-env.sh
spack tutorial -y
spack install lmod
spack install python

cp $HOME/buildtest/scripts/spack_container/modules.yaml $SPACK_ROOT/etc/spack/
spack module tcl refresh -y --delete-tree