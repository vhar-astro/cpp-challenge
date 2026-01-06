#include <gtest/gtest.h>

#include "mylib/sum.h"

TEST(SumTest, AddsTwoNumbers) {
  EXPECT_EQ(mylib::sum(2, 3), 5);
  EXPECT_EQ(mylib::sum(-1, 1), 0);
}

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
