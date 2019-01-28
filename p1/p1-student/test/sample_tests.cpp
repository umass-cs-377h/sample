#include <gtest/gtest.h>
#include <fstream>
#include <iostream>
#include <string>

#include "../src/sample.h"

using namespace std;

const string EXPECTED_STR =
    "Hello World";

TEST(SampleTest, Test1) {
  string out = go();
  EXPECT_EQ(out, EXPECTED_STR);
}

int main(int argc, char **argv) {
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
