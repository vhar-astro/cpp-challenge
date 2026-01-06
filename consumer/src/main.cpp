#include <cstdlib>
#include <iostream>

#include "mylib/sum.h"

int main() {
  int value = mylib::sum(10, 5);
  std::cout << "sum(10, 5)=" << value << "\n";
  return value == 15 ? EXIT_SUCCESS : EXIT_FAILURE;
}
