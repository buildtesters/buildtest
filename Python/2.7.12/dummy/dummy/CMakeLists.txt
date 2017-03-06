add_test(NAME Python-2.7.12-dummy-dummy-pip	COMMAND sh pip.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME Python-2.7.12-dummy-dummy-python	COMMAND sh python.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
