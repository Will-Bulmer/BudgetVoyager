#include <iostream>
#include <cstdlib>

int main() {
    int return_value = system("cmake --build ../build --target run_gui_script");
    
    if (return_value != 0) {
        std::cerr << "Error occurred while running the GUI script." << std::endl;
        return 1;
    } else {
        std::cout << "GUI script executed successfully." << std::endl;
    }

    return 0;
}
