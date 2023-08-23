# NOTE: Cannot find file: /home/will_bulmer/PROJECTS/BudgetVoyager/build/DartConfiguration.tcl 
# This is for CDash for continuous integration.

cmake_minimum_required(VERSION 3.10)

project(BudgetVoyager)

# C++ EXECUTABLES
# add_executable(runAlgorithm src/main.cpp) # Needs a main function before we add it

# PACKAGES
find_package(Catch2 REQUIRED)
find_package(Python3 COMPONENTS Interpreter)

# INCLUDE DIRECTORIES FOR EXECUTABLES
# target_include_directories(runAlgorithm PRIVATE ${CMAKE_SOURCE_DIR}/input)

# TESTING
enable_testing()

# CATCH
add_executable(tests_cpp tests/catch/some_test.cpp) # some_test.cpp
target_link_libraries(tests_cpp PRIVATE Catch2::Catch2)
add_test(NAME cpp_test COMMAND tests_cpp)

# PYTEST
# Called on 'ctest' or VS Code `Run CTest`
if(Python3_Interpreter_FOUND)
    add_test(NAME pytest_can_webscrape COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/tests/pytest/can_webscrape.py)
    #add_test(NAME pytest_can_otherTest COMMAND python -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/tests/pytest/otherTest.py)
endif()
