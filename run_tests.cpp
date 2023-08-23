#include <iostream>
#include <cstdlib>

int main() {
    int return_value = system("cd /home/will_bulmer/PROJECTS/BudgetVoyager/build && ctest");
    
    if (return_value != 0) {
        std::cerr << "Error occurred while running the tests." << std::endl;
    } else {
        std::cout << "Tests executed successfully." << std::endl;
    }

    return 0;
}
