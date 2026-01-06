cmake_minimum_required(VERSION 3.20)

file(READ "${CMAKE_CURRENT_SOURCE_DIR}/VERSION" PROJECT_VERSION_STRING)
string(STRIP "${PROJECT_VERSION_STRING}" PROJECT_VERSION_STRING)

project(mylib VERSION ${PROJECT_VERSION_STRING} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(MYLIB_BUILD_TESTS "Build mylib tests" ON)

include(GNUInstallDirs)
add_library(mylib src/sum.cpp)
target_include_directories(mylib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
set_target_properties(mylib PROPERTIES EXPORT_NAME mylib)

install(TARGETS mylib
        EXPORT mylibTargets
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/mylibConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion)

configure_package_config_file(
  cmake/mylibConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/mylibConfig.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/mylib)

install(EXPORT mylibTargets
        NAMESPACE mylib::
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/mylib)
install(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/mylibConfig.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/mylibConfigVersion.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/mylib)

if(MYLIB_BUILD_TESTS)
  enable_testing()
  find_package(GTest CONFIG REQUIRED)
  add_executable(mylib_tests tests/sum_test.cpp)
  target_link_libraries(mylib_tests PRIVATE GTest::gtest_main mylib)
  include(GoogleTest)
  gtest_discover_tests(mylib_tests)
endif()
