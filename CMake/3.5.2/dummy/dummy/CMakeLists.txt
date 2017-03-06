add_test(NAME CMake-3.5.2-dummy-dummy-cmake	COMMAND sh cmake.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME CMake-3.5.2-dummy-dummy-ccmake	COMMAND sh ccmake.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
add_test(NAME CMake-3.5.2-dummy-dummy-ctest	COMMAND sh ctest.sh 	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
