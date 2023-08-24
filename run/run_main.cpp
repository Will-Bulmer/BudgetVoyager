#include <iostream>
#include <cstdlib>

int main() {
    //int return_value = system("cd /home/will_bulmer/PROJECTS/BudgetVoyager/build && cmake --build . --target run_main_script");
    int return_value = system("cmake --build /home/will_bulmer/PROJECTS/BudgetVoyager/build --target run_main_script");
    

    
    if (return_value != 0) {
        std::cerr << "Error occurred while running the tests." << std::endl;
    } else {
        std::cout << "Tests executed successfully." << std::endl;
    }

    return 0;
}