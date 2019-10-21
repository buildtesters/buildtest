!*****************************************************************************
! FILE: omp_dotprod_serial.f
! DESCRIPTION:
!   This simple program is the serial version of a dot product and the
!   first of four codes used to show the progression from a serial program to a 
!   hybrid MPI/OpenMP program.  The relevant codes are:
!      - omp_dotprod_serial.f  - Serial version
!      - omp_dotprod_openmp.f  - OpenMP only version
!      - omp_dotprod_mpi.f     - MPI only version
!      - omp_dotprod_hybrid.f  - Hybrid MPI and OpenMP version
! SOURCE: Blaise Barney
! LAST REVISED:  06/02/17 Blaise Barney
!******************************************************************************

      program dotprod

! Define length of dot product vectors 
      integer VECLEN
      parameter(VECLEN=100)

      integer i
      real*8 a(VECLEN), b(VECLEN), sum

      print *, 'Starting omp_dotprod_serial'

! Initialize dot product vectors 
      do i=1, VECLEN
        a(i)=1.0
        b(i)=a(i)
      end do 

! Perform the dot product
      sum = 0.0
      do i=1, VECLEN
        sum = sum + a(i) * b(i)
      end do

      print *, 'Done. Serial version: sum  =', sum

      end
