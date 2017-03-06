add_test(NAME ifort-2017.1.132-GCC-5.2.0-dummy-dummy-ifort	COMMAND sh ifort.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME ifort-2017.1.132-GCC-5.2.0-dummy-dummy-hello_fortran	COMMAND sh hello_fortran.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
