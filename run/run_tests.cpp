#include <iostream>
#include <cstdlib>

int main() {
    // Assume the executable is run from the BudgetVoyager directory
    int run_tests = system("cd build && ctest");

    if (run_tests != 0) {
        std::cerr << "Some tests failed. Rerunning failed tests..." << std::endl;
        int rerun_failed_tests = system("cd build && ctest --rerun-failed --output-on-failure");

        if (rerun_failed_tests != 0) {
            std::cerr << "Error occurred while rerunning the failed tests." << std::endl;
            return 1;
        }
    }

    std::cout << "Tests executed successfully." << std::endl;

    return 0;
}
