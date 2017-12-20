buildtest -s GCC/5.4.0-2.27 --shell csh
buildtest -s OpenMPI/2.0.0 -t GCC/5.4.0-2.27 --testset MPI --job-template template/job.lsf
buildtest -s Python/2.7.12 -t intel/2017.01 --testset Python
buildtest -s R/3.3.1 -t intel/2017.01 --testset R
buildtest --system all
buildtest --system gcc
buildtest -s intel/2017.01 
buildtest -s Ruby/2.3.4 --testset Ruby
buildtest -s Perl/5.22.1 -t foss/.2016.03 --testset Perl
buildtest -s Tcl/.8.6.5 -t intel/2017.01
buildtest -s Tcl/.8.6.5 -t intel/2017.01 --testset Tcl


