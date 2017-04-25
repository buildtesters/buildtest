C *****************************************************************************
C FILE: mpi_array.f
C DESCRIPTION:
C   MPI Example - Array Assignment - Fortran Version
C   This program demonstrates a simple data decomposition. The master task 
C   first initializes an array and then distributes an equal portion that
C   array to the other tasks. After the other tasks receive their portion
C   of the array, they perform an addition operation to each array element.
C   They also maintain a sum for their portion of the array. The master task
C   does likewise with its portion of the array. As each of the non-master
C   tasks finish, they send their updated portion of the array to the master.
C   An MPI collective communication call is used to collect the sums
C   maintained by each task.  Finally, the master task displays selected
C   parts of the final array and the global sum of all array elements.
C   NOTE: the number of MPI tasks must be evenly divided by 4.
C AUTHOR: Blaise Barney
C LAST REVISED: 01/24/09
C **************************************************************************

      program array 
      include 'mpif.h'

      integer   ARRAYSIZE, MASTER
      parameter (ARRAYSIZE = 16000000)
      parameter (MASTER = 0)

      integer  numtasks, taskid, ierr, dest, offset, i, tag1,
     &         tag2, source, chunksize
      real*4   mysum, sum, data(ARRAYSIZE)
      integer  status(MPI_STATUS_SIZE)
      common   /a/ data

C ***** Initializations *****
      call MPI_INIT(ierr)
      call MPI_COMM_SIZE(MPI_COMM_WORLD, numtasks, ierr)
      i = MOD(numtasks, 4)
      if (i .ne. 0) then
        call MPI_Abort(MPI_COMM_WORLD,ierr)
        stop
      end if
      call MPI_COMM_RANK(MPI_COMM_WORLD, taskid, ierr)
      write(*,*)'MPI task',taskid,'has started...'
      chunksize = (ARRAYSIZE / numtasks)
      tag2 = 1
      tag1 = 2

C***** Master task only ******
      if (taskid .eq. MASTER) then

C       Initialize the array
        sum = 0.0
        do i=1, ARRAYSIZE 
          data(i) = i * 1.0
          sum = sum + data(i)
        end do
        write(*,20) sum

C       Send each task its portion of the array - master keeps 1st part
        offset = chunksize + 1
        do dest=1, numtasks-1
          call MPI_SEND(offset, 1, MPI_INTEGER, dest, tag1, 
     &      MPI_COMM_WORLD, ierr)
          call MPI_SEND(data(offset), chunksize, MPI_REAL, dest, 
     &      tag2, MPI_COMM_WORLD, ierr)
          write(*,*) 'Sent',chunksize,'elements to task',dest,
     &      'offset=',offset
          offset = offset + chunksize
        end do

C       Master does its part of the work
        offset = 1
        call update(offset, chunksize, taskid, mysum)

C       Wait to receive results from each task
        do i=1, numtasks-1
          source = i
          call MPI_RECV(offset, 1, MPI_INTEGER, source, tag1,
     &      MPI_COMM_WORLD, status, ierr)
          call MPI_RECV(data(offset), chunksize, MPI_REAL, 
     &      source, tag2, MPI_COMM_WORLD, status, ierr)
        end do 

C       Get final sum and print sample results
        call MPI_Reduce(mysum, sum, 1, MPI_REAL, MPI_SUM, MASTER,
     &    MPI_COMM_WORLD, ierr)
        print *, 'Sample results:'
        offset = 1
        do i=1, numtasks
          write (*,30) data(offset:offset+4)
          offset = offset + chunksize
        end do
        write(*,40) sum

      end if


C***** Non-master tasks only *****

      if (taskid .gt. MASTER) then

C       Receive my portion of array from the master task */
        call MPI_RECV(offset, 1, MPI_INTEGER, MASTER, tag1,
     &    MPI_COMM_WORLD, status, ierr)
        call MPI_RECV(data(offset), chunksize, MPI_REAL, MASTER,
     &    tag2, MPI_COMM_WORLD, status, ierr)

        call update(offset, chunksize, taskid, mysum)

C       Send my results back to the master
        call MPI_SEND(offset, 1, MPI_INTEGER, MASTER, tag1,
     &    MPI_COMM_WORLD, ierr)
        call MPI_SEND(data(offset), chunksize, MPI_REAL, MASTER,
     &    tag2, MPI_COMM_WORLD, ierr)

        call MPI_Reduce(mysum, sum, 1, MPI_REAL, MPI_SUM, MASTER,
     &    MPI_COMM_WORLD, ierr)

      endif


      call MPI_FINALIZE(ierr)

  20  format('Initialized array sum = ',E12.6)
  30  format(5E14.6) 
  40  format('*** Final sum= ',E12.6,' ***')

      end




      subroutine update(myoffset, chunksize, myid, mysum)
        integer   ARRAYSIZE, myoffset, chunksize, myid, i
        parameter (ARRAYSIZE = 16000000)
        real*4 mysum, data(ARRAYSIZE)
        common /a/ data
C       Perform addition to each of my array elements and keep my sum
        mysum = 0 
        do i=myoffset, myoffset + chunksize-1
          data(i) = data(i) + i * 1.0 
          mysum = mysum + data(i)
        end do
        write(*,50) myid,mysum
  50    format('Task',I4,' mysum = ',E12.6) 
      end subroutine update

 

