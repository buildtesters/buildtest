!*****************************************************************************
! FILE: omp_dotprod_mpi.f
! DESCRIPTION:
!   This simple program is the MPI version of a dot product and the third
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

! Define length of dot product vectors 
      integer VECLEN
      parameter(VECLEN=100)

      integer i, myid, numprocs, ierr
      real*8 a(VECLEN), b(VECLEN), mysum, allsum

! MPI Initialization 
      call MPI_INIT (ierr)
      call MPI_COMM_SIZE (MPI_COMM_WORLD, numprocs,ierr)
      call MPI_COMM_RANK (MPI_COMM_WORLD, myid, ierr)

! Each MPI task performs the dot product, obtains its partial sum, and then calls
! MPI_Reduce to obtain the global sum.
      if (myid .eq. 0) then
        print *, 'Starting omp_dotprod_mpi. Using',numprocs,' tasks...'
      end if

! Initialize dot product vectors 
      do i=1, VECLEN
        a(i)=1.0
        b(i)=a(i)
      end do 

! Perform the dot product
      mysum = 0.0
      do i=1, VECLEN
        mysum = mysum + a(i) * b(i)
      end do

      print *,'Task',myid,' partial sum =',mysum

! After the dot product, perform a summation of results on each node 
      call MPI_REDUCE (mysum, allsum, 1, MPI_DOUBLE_PRECISION, MPI_SUM, 
     &            0, MPI_COMM_WORLD, ierr);
      if (myid .eq. 0) then
        print *, 'Done. MPI version: global sum  =', allsum
      end if

      call MPI_FINALIZE(ierr)

      end
