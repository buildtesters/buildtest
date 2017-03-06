add_test(NAME icc-2017.1.132-GCC-5.2.0-dummy-dummy-icc	COMMAND sh icc.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME icc-2017.1.132-GCC-5.2.0-dummy-dummy-icpc	COMMAND sh icpc.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME icc-2017.1.132-GCC-5.2.0-dummy-dummy-hello_c	COMMAND sh hello_c.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME icc-2017.1.132-GCC-5.2.0-dummy-dummy-hello_cpp	COMMAND sh hello_cpp.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
