cmake_minimum_required(VERSION 3.14)
project(gdb_armadillo_helpers)

set(CMAKE_CXX_STANDARD 17)

# xxxxxxxxxx Conan xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
if(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
  include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
  conan_basic_setup(TARGETS)
else()
  message(FATAL_ERROR "The file conanbuildinfo.cmake doesn't exist! Run the command below from conan folder
    conan install .. --build=missing -s build_type=Release")
endif()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

add_executable(gdb_armadillo_helpers main.cpp)
target_link_libraries(gdb_armadillo_helpers CONAN_PKG::armadillo)
