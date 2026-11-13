// Copyright 2023 Picknik Robotics
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//    * Redistributions of source code must retain the above copyright
//      notice, this list of conditions and the following disclaimer.
//
//    * Redistributions in binary form must reproduce the above copyright
//      notice, this list of conditions and the following disclaimer in the
//      documentation and/or other materials provided with the distribution.
//
//    * Neither the name of the PickNik Inc. nor the names of its
//      contributors may be used to endorse or promote products derived from
//      this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
//
// Author: Chance Cardona
//

#include <limits>
#include <memory>

#include "generate_parameter_library_example/admittance_controller_parameters.hpp"
#include "gtest/gtest.h"
#include "rclcpp/rclcpp.hpp"

class DescriptorTest : public ::testing::Test {
 public:
  void SetUp() {
    example_test_node_ = std::make_shared<rclcpp::Node>("example_test_node");

    std::shared_ptr<admittance_controller::ParamListener> param_listener =
        std::make_shared<admittance_controller::ParamListener>(
            example_test_node_->get_node_parameters_interface());
    params_ = param_listener->get_params();
    std::vector<std::string> names = {"admittance.damping_ratio", "one_number",
                                      "pid.joint4.p", "lt_eq_fifteen",
                                      "gt_fifteen"};
    descriptors_ = example_test_node_->describe_parameters(names);
  }

  void TearDown() { example_test_node_.reset(); }

 protected:
  std::shared_ptr<rclcpp::Node> example_test_node_;
  admittance_controller::Params params_;
  std::vector<rcl_interfaces::msg::ParameterDescriptor> descriptors_;
};

// Checks element_bounds<> on a float
TEST_F(DescriptorTest, check_floating_point_descriptors) {
  EXPECT_EQ(descriptors_[0].floating_point_range.at(0).from_value, 0.1);
  EXPECT_EQ(descriptors_[0].floating_point_range.at(0).to_value, 10);
}

// Checks bounds<> on an int
TEST_F(DescriptorTest, check_integer_descriptors) {
  EXPECT_EQ(descriptors_[1].integer_range.at(0).from_value, 1024);
  EXPECT_EQ(descriptors_[1].integer_range.at(0).to_value, 65535);
}

TEST_F(DescriptorTest, check_lower_upper_bounds) {
  EXPECT_EQ(descriptors_[2].floating_point_range.at(0).from_value, 0.0001);
  EXPECT_EQ(descriptors_[2].floating_point_range.at(0).to_value,
            std::numeric_limits<double>::infinity());
}

TEST_F(DescriptorTest, check_lt_eq) {
  EXPECT_EQ(descriptors_[3].integer_range.at(0).from_value,
            std::numeric_limits<int64_t>::lowest());
  EXPECT_EQ(descriptors_[3].integer_range.at(0).to_value, 15);
}

TEST_F(DescriptorTest, check_gt) {
  EXPECT_EQ(descriptors_[4].integer_range.at(0).from_value, 16);
  EXPECT_EQ(descriptors_[4].integer_range.at(0).to_value,
            std::numeric_limits<int64_t>::max());
}

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  rclcpp::init(argc, argv);
  int result = RUN_ALL_TESTS();
  rclcpp::shutdown();
  return result;
}
