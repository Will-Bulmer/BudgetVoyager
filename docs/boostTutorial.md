## A Simple Tutorial on the Boost Library

## C++ FUNCTION TO PYTHON

1. **Write a C++ function to expose to Python**
Let's create a simple function that we want to expose. Name the file `hello_ext.cpp`.
```cpp
#include <boost/python.hpp>

char const* greet() {
   return "Hello, Boost.Python!";
}

BOOST_PYTHON_MODULE(hello_ext) {
    using namespace boost::python;
    def("greet", greet);
}
```
In this code, we defined a simple function `greet()` that returns a string. We then used the `BOOST_PYTHON_MODULE` macro to create a Python module named `hello_ext`, and exposed the `greet()` function using the `def` function.

2. **Compile the C++ code into a shared library**
To compile the code, you'll need to ensure you have the right paths to the Boost.Python and Python libraries and headers. Here's a simple `g++` command for this:
```bash
g++ -shared -fPIC -I/usr/include/python3.8 -I/path_to_boost -L/usr/lib/python3.8/config-3.8-x86_64-linux-gnu -lboost_python38 -lpython3.8 -o hello_ext.so hello_ext.cpp
```
Replace `/path_to_boost` with the path to your Boost installation, and adjust the Python version (e.g., 3.8) as necessary.

3. **Using the Extension in Python**
With the shared library (`hello_ext.so`) built, you can import and use it in Python:
```python
import hello_ext

print(hello_ext.greet())  # Output: Hello, Boost.Python!
```

4. **CMAKE file:**
```cmake
cmake_minimum_required(VERSION 3.10)

project(HelloBoostPython)

# Specify the required C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find Python interpreter, libraries, and headers
find_package(PythonLibs 3 REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

# Find Boost and Boost.Python
find_package(Boost REQUIRED COMPONENTS python)

# Create the Python module
add_library(hello_ext MODULE hello_ext.cpp)
target_link_libraries(hello_ext Boost::python ${PYTHON_LIBRARIES})
set_target_properties(hello_ext PROPERTIES PREFIX "")
```

## PYTHON FUNCTION TO C++

1. **Write a Python function**
Save this function to a file named `python_func.py`:
```python
def greet(name):
    return f"Hello, {name}!"
```

2. **Write a C++ program to call this Python function**
Create a file named `main.cpp`:
```cpp
#include <iostream>
#include <string>
#include <boost/python.hpp>

int main() {
    Py_Initialize();

    // Add the current directory to the sys.path to ensure our Python module can be found
    boost::python::exec("import sys\nsys.path.append('.')");

    // Load the python module
    boost::python::object python_func_module = boost::python::import("python_func");

    // Get the greet function from the module
    boost::python::object greet_func = python_func_module.attr("greet");

    // Call the greet function with a string argument
    boost::python::object result = greet_func("Boost.Python");
    std::cout << boost::python::extract<std::string>(result) << std::endl;

    Py_Finalize();
    return 0;
}
```

3. **CMAKE File for building the C++ program**
Here's a `CMakeLists.txt` to build the above C++ program:
```cmake
cmake_minimum_required(VERSION 3.10)

project(CallPythonFromCpp)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(PythonLibs 3 REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

find_package(Boost REQUIRED COMPONENTS python)

add_executable(call_python main.cpp)
target_link_libraries(call_python Boost::python ${PYTHON_LIBRARIES})
```

## Example at Converting Python List to C Vector
```cpp
#include <vector>
#include <iostream>
#include <boost/python.hpp>

namespace py = boost::python;

std::vector<double> process_data(const py::list& dataList) {
    std::vector<double> data;
    for(int i = 0; i < py::len(dataList); ++i) {
        data.push_back(py::extract<double>(dataList[i]));
    }
    
    // Your algorithm to process data
    for(auto& num : data) {
        num *= 2;  // Just a simple example of doubling the number
    }

    return data;
}

BOOST_PYTHON_MODULE(algo) {
    py::def("process_data", process_data);
}
```
In the above C++ code, we define a function `process_data` that takes a Python list as input, converts it into a C++ `std::vector`, processes the data, and returns the processed data as a `std::vector`.