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

# Adding a target for the Python script
add_custom_target(run_main_script
    COMMAND ${CMAKE_COMMAND} -E env "PYTHONPATH=${CMAKE_SOURCE_DIR}/input:$ENV{PYTHONPATH}" ${CMAKE_SOURCE_DIR}/src/main.py
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Executing main.py"
    VERBATIM
)





# TESTING
enable_testing()

# CATCH
add_executable(test_cpp tests/catch/some_test.cpp) # some_test.cpp
target_include_directories(test_cpp PRIVATE ${CMAKE_SOURCE_DIR}/input)
target_link_libraries(test_cpp PRIVATE Catch2::Catch2)
add_test(NAME cpp_test COMMAND test_cpp)

# PYTEST
# Called on 'ctest' or VS Code `Run CTest`
if(Python3_Interpreter_FOUND)
    add_test(
        NAME pytest_can_webscrape
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/tests/pytest/test_can_webscrape.py
    )
    # Setting the PYTHONPATH to include the input directory
    set_tests_properties(pytest_can_webscrape 
        PROPERTIES 
        ENVIRONMENT "PYTHONPATH=${CMAKE_SOURCE_DIR}/input:$ENV{PYTHONPATH}"
    )
    # Uncomment below when you have other Python tests
    # add_test(NAME pytest_can_otherTest COMMAND python -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/tests/pytest/otherTest.py)
endif()
