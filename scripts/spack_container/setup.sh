#cp $HOME/buildtest/scripts/spack_container/modules.yaml $SPACK_ROOT/etc/spack
# spack module tcl refresh --delete-tree -y
module load python
cd $HOME/buildtest
#rm -rf $HOME/buildtest/.packages

export PATH=$HOME/.local/bin:$PATH
# user installed python libraries need to be added to PYTHON path for running regression test
export PYTHONPATH=$HOME/.local/lib/python3.6/site-packages:$PYTHONPATH
source setup.sh
pip uninstall -y dataclasses
export BUILDTEST_CONFIGFILE=$HOME/buildtest/buildtest/settings/spack_container.yml
