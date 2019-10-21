/*****************************************************************************
* FILE: omp_dotprod_hybrid.c
* DESCRIPTION:
*   This simple program is the hybrid version of a dot product and the fourth
*   of four codes used to show the progression from a serial program to a 
*   hybrid MPI/OpenMP program.  The relevant codes are:
*      - omp_dotprod_serial.c  - Serial version
*      - omp_dotprod_openmp.c  - OpenMP only version
*      - omp_dotprod_mpi.c     - MPI only version
*      - omp_dotprod_hybrid.c  - Hybrid MPI and OpenMP version
* SOURCE: Blaise Barney
* LAST REVISED:  06/02/17 Blaise Barney
******************************************************************************/

#include <mpi.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

/* Define length of dot product vectors and number of OpenMP threads */
#define VECLEN 100
#define NUMTHREADS 8

int main (int argc, char* argv[])
{
int i, myid, tid, numprocs, len=VECLEN, threads=NUMTHREADS;
double *a, *b;
double mysum, allsum, sum, psum;

/* MPI Initialization */
MPI_Init (&argc, &argv);
MPI_Comm_size (MPI_COMM_WORLD, &numprocs);
MPI_Comm_rank (MPI_COMM_WORLD, &myid);

/* 
   Each MPI task uses OpenMP to perform the dot product, obtains its partial sum, 
   and then calls MPI_Reduce to obtain the global sum.
*/
if (myid == 0)
  printf("Starting omp_dotprod_hybrid. Using %d tasks...\n",numprocs);

/* Assign storage for dot product vectors */
a = (double*) malloc (len*threads*sizeof(double));
b = (double*) malloc (len*threads*sizeof(double));
 
/* Initialize dot product vectors */
for (i=0; i<len*threads; i++) {
  a[i]=1.0;
  b[i]=a[i];
  }

/*
   Perform the dot product in an OpenMP parallel region for loop with a sum reduction
   For illustration purposes:
     - Explicitly sets number of threads
     - Gets and prints number of threads used
     - Each thread keeps track of its partial sum
*/

/* Initialize OpenMP reduction sum */
sum = 0.0;

#pragma omp parallel private(i,tid,psum) num_threads(threads)
{
psum = 0.0;
tid = omp_get_thread_num();
if (tid ==0)
  {
    threads = omp_get_num_threads();
    printf("Task %d using %d threads\n",myid, threads);
  }

#pragma omp for reduction(+:sum)
  for (i=0; i<len*threads; i++)
    {
      sum += (a[i] * b[i]);
      psum = sum;
    }
printf("Task %d thread %d partial sum = %f\n",myid, tid, psum);
}


/* Print this task's partial sum */
mysum = sum;
printf("Task %d partial sum = %f\n",myid, mysum);

/* After the dot product, perform a summation of results on each node */
MPI_Reduce (&mysum, &allsum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
if (myid == 0) 
  printf ("Done. Hybrid version: global sum  =  %f \n", allsum);

free (a);
free (b);
MPI_Finalize();
}   
