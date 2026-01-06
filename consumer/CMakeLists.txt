cmake_minimum_required(VERSION 3.20)
project(mylib-consumer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(mylib CONFIG REQUIRED)

add_executable(consumer src/main.cpp)
target_link_libraries(consumer PRIVATE mylib::mylib)

include(CTest)
add_test(NAME consumer_runs COMMAND consumer)
