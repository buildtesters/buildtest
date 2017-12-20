# these test should all fail

buildtest --system xxx
buildtest -s GCC/5.4.0-2.27 -t 
buildtest -s GCC/5.4.0-2.27 -t intel/2017.01
buildtest -s OpenMPI/2.0.2 -t GCCcore/.5.4.0
buildtest --system firefox --job-template /etc/fstab
buildtest --system firefox --job-template /etc/fstab.lsf
buildtest --system firefox --job-template $HOME/fstab.lsf
buildtest --system firefox --testset MPI
