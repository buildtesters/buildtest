# these test should all fail

./_buildtest --system xxx
./_buildtest -s GCC/6.4.0-2.28 -t 
./_buildtest --system firefox --job-template /etc/fstab
./_buildtest --system firefox --job-template /etc/fstab.lsf
./_buildtest --system firefox --job-template $HOME/fstab.lsf
./_buildtest --system firefox --testset MPI
buildtest -s GCC/5.4.0-2.27 -t intel/2017.01
buildtest -s OpenMPI/2.0.2 -t GCCcore/.5.4.0
