#include <mpi.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char** argv) {
    // Initialize the MPI environment
    MPI_Init(&argc,&argv);

    // Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // Get the name of the processor
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);


    //printf("%s rank %d out of %d processors: \n", processor_name, world_rank, world_size);
    // Print off a hello world message
    for (int i = 0; i < world_size; i++)
    {
	if (i == world_rank)
	{	
		char *temp; // = (char*)malloc(sizeof(char)*128);
		//char *temp="helloworld";
		for (int j = 1; j < argc; j++)
			temp=strcat(temp,argv[j]);
			temp=strcat(temp," ");
			
    	printf("%s rank %d out of %d processors:  %s \n", processor_name, world_rank, world_size,temp);
	
	}
    }

    // Finalize the MPI environment.
    MPI_Finalize();
}
