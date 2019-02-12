!*****************************************************************************
! FILE: omp_dotprod_openmp.f
! DESCRIPTION:
!   This simple program is the OpenMP version of a dot product and the
!   second of four codes used to show the progression from a serial program to a 
!   hybrid MPI/OpenMP program.  The relevant codes are:
!      - omp_dotprod_serial.f  - Serial version
!      - omp_dotprod_openmp.f  - OpenMP only version
!      - omp_dotprod_mpi.f     - MPI only version
!      - omp_dotprod_hybrid.f  - Hybrid MPI and OpenMP version
! SOURCE: Blaise Barney
! LAST REVISED:  06/02/17 Blaise Barney
!******************************************************************************

      program dotprod

! Define length of dot product vectors and number of OpenMP threads 
      integer VECLEN, NUMTHREADS
      parameter(VECLEN=100)
      parameter(NUMTHREADS=8)

      integer i, tid, OMP_GET_THREAD_NUM
      real*8 a(VECLEN*NUMTHREADS), b(VECLEN*NUMTHREADS), sum, psum

      print *, 'Starting omp_dotprod_openmp. Using',NUMTHREADS,
     &         ' threads'

! Initialize dot product vectors 
      do i=1, VECLEN*NUMTHREADS
        a(i)=1.0
        b(i)=a(i)
      end do 
! Initialize global sum
      sum = 0.0

! Perform the dot product in an OpenMP parallel region for loop with a sum reduction
! For illustration purposes:
!   - Explicitly sets number of threads
!   - Each thread keeps track of its partial sum

!$OMP PARALLEL PRIVATE(i,tid,psum) NUM_THREADS(NUMTHREADS)
      psum = 0.0
      tid = OMP_GET_THREAD_NUM()

!$OMP DO REDUCTION(+:sum)
      do i=1, VECLEN*NUMTHREADS
        sum = sum + a(i) * b(i)
        psum = sum
      end do
!$OMP END DO
      print *, 'Thread',tid,' partial sum =',psum
!$OMP END PARALLEL

      print *, 'Done. OpenMP version: sum  =', sum

      end
