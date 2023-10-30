#include <iostream>
#include <cstdlib>

int main() {
    int return_value = system("cmake --build ../build --target run_main_script");
    
    if (return_value != 0) {
        std::cerr << "Error occurred while running the main file." << std::endl;
        return 1;
    } else {
        std::cout << "Tests executed successfully." << std::endl;
    }

    return 0;
}
