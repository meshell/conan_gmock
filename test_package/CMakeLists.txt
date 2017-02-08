PROJECT(MyGMocktest)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(mytest test.cpp)

find_package(GMock REQUIRED)

if(GMOCK_FOUND)
    target_link_libraries(mytest
            GMock::GMock
            GMock::Main
            )
endif(GMOCK_FOUND)
