#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main (int argc, char *argv[])
{
  int tid;
  #pragma omp parallel private(tid)
  {
    tid = omp_get_thread_num();
    printf("Hello World from thread = %d\n", tid);

  }
}