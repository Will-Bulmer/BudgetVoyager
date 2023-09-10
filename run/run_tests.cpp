#include <iostream>
#include <cstdlib>

#include <iostream>
#include <cstdlib>

int main() {
    int run_tests = system("cd /home/will_bulmer/PROJECTS/BudgetVoyager/build && ctest");

    if (run_tests != 0) {
        std::cerr << "Some tests failed. Rerunning failed tests..." << std::endl;
        int rerun_failed_tests = system("cd /home/will_bulmer/PROJECTS/BudgetVoyager/build && ctest --rerun-failed --output-on-failure");

        if (rerun_failed_tests != 0) {
            std::cerr << "Error occurred while rerunning the failed tests." << std::endl;
            return 1;
        }
    }

    std::cout << "Tests executed successfully." << std::endl;

    return 0;
}

