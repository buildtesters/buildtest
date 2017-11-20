!*****************************************************************************
! FILE: omp_dotprod_hybrid.f
! DESCRIPTION:
!   This simple program is the hybrid version of a dot product and the fourth
!   of four codes used to show the progression from a serial program to a
!   hybrid MPI/OpenMP program.  The relevant codes are:
!      - omp_dotprod_serial.f  - Serial version
!      - omp_dotprod_openmp.f  - OpenMP only version
!      - omp_dotprod_mpi.f     - MPI only version
!      - omp_dotprod_hybrid.f  - Hybrid MPI and OpenMP version
! SOURCE: Blaise Barney
! LAST REVISED:  06/02/17 Blaise Barney
!******************************************************************************

      program dotprod
      include 'mpif.h'

! Define length of dot product vectors and number of OpenMP threads
      integer VECLEN, NUMTHREADS
      parameter(VECLEN=100)
      parameter(NUMTHREADS=8)

      integer i, myid, tid, numprocs, threads, ierr, OMP_GET_THREAD_NUM,
     &        OMP_GET_NUM_THREADS
      real*8 a(VECLEN*NUMTHREADS), b(VECLEN*NUMTHREADS)
      real*8 mysum, allsum, sum, psum

! MPI Initialization 
      call MPI_INIT (ierr)
      call MPI_COMM_SIZE (MPI_COMM_WORLD, numprocs,ierr)
      call MPI_COMM_RANK (MPI_COMM_WORLD, myid, ierr)

! Each MPI task uses OpenMP to perform the dot product, obtains its
! partial sum, and then calls MPI_Reduce to obtain the global sum.
      if (myid .eq. 0) then
        print *, 'Starting omp_dotprod_hybrid. Using',numprocs,
     &           ' tasks...'
      end if

! Initialize dot product vectors 
      do i=1, VECLEN*NUMTHREADS
        a(i)=1.0
        b(i)=a(i)
      end do 

! Perform the dot product in an OpenMP parallel region for loop with a sum reduction
! For illustration purposes:
!   - Explicitly sets number of threads
!   - Gets and prints number of threads used
!   - Each thread keeps track of its partial sum

! Initialize OpenMP reduction sum
      sum = 0.0

!$OMP PARALLEL PRIVATE(i,tid,psum) NUM_THREADS(NUMTHREADS)
      psum = 0.0
      tid = OMP_GET_THREAD_NUM()
      if (tid .eq. 0) then
        threads = OMP_GET_NUM_THREADS()
        print *,'Task',myid,' using',NUMTHREADS,' threads'
      end if

!$OMP DO REDUCTION(+:sum)
      do i=1, VECLEN*NUMTHREADS
        sum = sum + a(i) * b(i)
        psum = sum
      end do
!$OMP END DO
      print *, 'Task',myid,'thread',tid,' partial sum =',psum
!$OMP END PARALLEL

! Print this task's partial sum
      mysum = sum
      print *,'Task',myid,'partial sum =',mysum

! After the dot product, perform a summation of results on each node 
      call MPI_REDUCE (mysum, allsum, 1, MPI_DOUBLE_PRECISION, MPI_SUM, 
     &            0, MPI_COMM_WORLD, ierr);
      if (myid .eq. 0) then
        print *, 'Done. Hybrid version: global sum  =', allsum
      end if

      call MPI_FINALIZE(ierr)

      end
