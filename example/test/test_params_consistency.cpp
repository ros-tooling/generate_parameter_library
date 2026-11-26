// Copyright 2026 Generate Parameter Library Contributors
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
//    * Neither the name of the Generate Parameter Library contributors nor
//      the names of its contributors may be used to endorse or promote
//      products derived from this software without specific prior written
//      permission.
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

/**
 * Tests that verify consistency between get_params() (library internal state)
 * and node.get_parameter() (ROS2 parameter server) for admittance_controller.
 *
 * After ParamListener::__init__() calls declare_params(), all parameters
 * (static and dynamic map entries) are declared in the ROS2 node and read back
 * via get_parameter(), then stored in params_ via update_internal_params().
 * This test verifies both sources remain in sync under default values and after
 * updates via set_parameters().
 */

#include <cmath>
#include <memory>
#include <stdexcept>
#include <vector>

#include "generate_parameter_library_example/admittance_controller_parameters.hpp"
#include "gmock/gmock.h"
#include "rclcpp/rclcpp.hpp"

class TestParamsConsistency : public ::testing::Test {
 public:
  static void SetUpTestSuite() { rclcpp::init(0, nullptr); }

  static void TearDownTestSuite() { rclcpp::shutdown(); }

  void SetUp() override {
    // Create node with required parameters
    node_ = std::make_shared<rclcpp::Node>(
        "test_admittance_controller",
        rclcpp::NodeOptions()
            .automatically_declare_parameters_from_overrides(true)
            .parameter_overrides({
                rclcpp::Parameter("fixed_string_no_default", "happy"),
                rclcpp::Parameter(
                    "fixed_string_array_no_default",
                    std::vector<std::string>{"alpha", "beta", "gamma", "delta",
                                             "epsilon"}),
                rclcpp::Parameter("command_interfaces",
                                  std::vector<std::string>{"position"}),
                rclcpp::Parameter(
                    "state_interfaces",
                    std::vector<std::string>{"position", "velocity"}),
                rclcpp::Parameter(
                    "chainable_command_interfaces",
                    std::vector<std::string>{"position", "velocity"}),
                rclcpp::Parameter("kinematics.plugin_name",
                                  "kdl_plugin/KDLKinematics"),
                rclcpp::Parameter("kinematics.plugin_package",
                                  "kinematics_interface_kdl"),
                rclcpp::Parameter("kinematics.base", "base_link"),
                rclcpp::Parameter("kinematics.tip", "ee_link"),
                rclcpp::Parameter("kinematics.group_name", "manipulator"),
                rclcpp::Parameter("ft_sensor.name", "tcp_fts_sensor"),
                rclcpp::Parameter("ft_sensor.frame.id", "ee_link"),
                rclcpp::Parameter("control.frame.id", "ee_link"),
                rclcpp::Parameter("fixed_world_frame.frame.id", "base_link"),
                rclcpp::Parameter("gravity_compensation.frame.id", "ee_link"),
                rclcpp::Parameter("gravity_compensation.CoG.pos",
                                  std::vector<double>{0.1, 0.0, 0.0}),
                rclcpp::Parameter(
                    "admittance.selected_axes",
                    std::vector<bool>{true, true, true, true, true, true}),
                rclcpp::Parameter(
                    "admittance.mass",
                    std::vector<double>{3.0, 3.0, 3.0, 3.0, 3.0, 3.0}),
                rclcpp::Parameter(
                    "admittance.damping_ratio",
                    std::vector<double>{2.828427, 2.828427, 2.828427, 2.828427,
                                        2.828427, 2.828427}),
                rclcpp::Parameter(
                    "admittance.stiffness",
                    std::vector<double>{50.0, 50.0, 50.0, 1.0, 1.0, 1.0}),
            }));

    param_listener_ = std::make_shared<admittance_controller::ParamListener>(
        node_->get_node_parameters_interface());
    params_ = param_listener_->get_params();
  }

  void TearDown() override {
    node_.reset();
    param_listener_.reset();
  }

 protected:
  std::shared_ptr<rclcpp::Node> node_;
  std::shared_ptr<admittance_controller::ParamListener> param_listener_;
  admittance_controller::Params params_;
};

// =========================================================================
// Static / Flat Parameters Tests
// =========================================================================

TEST_F(TestParamsConsistency, ScientificNotationNum) {
  EXPECT_DOUBLE_EQ(params_.scientific_notation_num,
                   node_->get_parameter("scientific_notation_num").as_double());
}

TEST_F(TestParamsConsistency, InterpolationMode) {
  EXPECT_EQ(params_.interpolation_mode,
            node_->get_parameter("interpolation_mode").as_string());
}

TEST_F(TestParamsConsistency, ControlMode) {
  EXPECT_EQ(params_.control_mode,
            admittance_controller::Params::ControlMode::position);
  EXPECT_EQ(to_string(params_.control_mode),
            node_->get_parameter("control_mode").as_string());
  EXPECT_EQ(param_listener_->get_stack_params().control_mode,
            params_.control_mode);
}

TEST_F(TestParamsConsistency, ControlModeStringConversions) {
  using admittance_controller::Params;
  EXPECT_EQ(admittance_controller::from_string<Params::ControlMode>("velocity"),
            Params::ControlMode::velocity);
  EXPECT_THROW(
      (void)admittance_controller::from_string<Params::ControlMode>("torque"),
      std::invalid_argument);
}

TEST_F(TestParamsConsistency, SubsetSelection) {
  auto param_vec = node_->get_parameter("subset_selection").as_string_array();
  EXPECT_THAT(params_.subset_selection, ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, Joints) {
  auto param_vec = node_->get_parameter("joints").as_string_array();
  EXPECT_THAT(params_.joints, ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, DofNames) {
  auto param_vec = node_->get_parameter("dof_names").as_string_array();
  EXPECT_THAT(params_.dof_names, ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, FixedString) {
  EXPECT_EQ(rsl::to_string(params_.fixed_string),
            node_->get_parameter("fixed_string").as_string());
}

TEST_F(TestParamsConsistency, FixedArray) {
  auto param_vec = node_->get_parameter("fixed_array").as_double_array();
  auto params_vec = rsl::to_vector(params_.fixed_array);
  EXPECT_THAT(params_vec, ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, FixedBoolArray) {
  auto param_vec = node_->get_parameter("fixed_bool_array").as_bool_array();
  auto params_vec = rsl::to_vector(params_.fixed_bool_array);
  EXPECT_THAT(params_vec, ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, EnableParameterUpdateWithoutReactivation) {
  EXPECT_EQ(params_.enable_parameter_update_without_reactivation,
            node_->get_parameter("enable_parameter_update_without_reactivation")
                .as_bool());
}

TEST_F(TestParamsConsistency, UseFeedforwardCommandedInput) {
  EXPECT_EQ(params_.use_feedforward_commanded_input,
            node_->get_parameter("use_feedforward_commanded_input").as_bool());
}

TEST_F(TestParamsConsistency, LtEqFifteen) {
  EXPECT_EQ(params_.lt_eq_fifteen,
            node_->get_parameter("lt_eq_fifteen").as_int());
}

TEST_F(TestParamsConsistency, GtFifteen) {
  EXPECT_EQ(params_.gt_fifteen, node_->get_parameter("gt_fifteen").as_int());
}

TEST_F(TestParamsConsistency, OneNumber) {
  EXPECT_EQ(params_.one_number, node_->get_parameter("one_number").as_int());
}

TEST_F(TestParamsConsistency, ThreeNumbers) {
  auto param_vec = node_->get_parameter("three_numbers").as_integer_array();
  auto params_vec = params_.three_numbers;
  EXPECT_THAT(params_vec, ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, ThreeNumbersOfFive) {
  auto param_vec =
      node_->get_parameter("three_numbers_of_five").as_integer_array();
  auto params_vec = rsl::to_vector(params_.three_numbers_of_five);
  EXPECT_THAT(params_vec, ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, HoverOverride) {
  EXPECT_EQ(params_.hover_override,
            node_->get_parameter("hover_override").as_int());
}

TEST_F(TestParamsConsistency, AngleWraparound) {
  EXPECT_EQ(params_.angle_wraparound,
            node_->get_parameter("angle_wraparound").as_bool());
}

TEST_F(TestParamsConsistency, OpenLoopControl) {
  EXPECT_EQ(params_.open_loop_control,
            node_->get_parameter("open_loop_control").as_bool());
}

// =========================================================================
// Nested Struct Parameters Tests
// =========================================================================

TEST_F(TestParamsConsistency, PidRate) {
  EXPECT_DOUBLE_EQ(params_.pid.rate,
                   node_->get_parameter("pid.rate").as_double());
}

TEST_F(TestParamsConsistency, KinematicsAlpha) {
  EXPECT_DOUBLE_EQ(params_.kinematics.alpha,
                   node_->get_parameter("kinematics.alpha").as_double());
}

TEST_F(TestParamsConsistency, FtSensorFilterCoefficient) {
  EXPECT_DOUBLE_EQ(
      params_.ft_sensor.filter_coefficient,
      node_->get_parameter("ft_sensor.filter_coefficient").as_double());
}

TEST_F(TestParamsConsistency, FtSensorFrameExternal) {
  EXPECT_EQ(params_.ft_sensor.frame.external,
            node_->get_parameter("ft_sensor.frame.external").as_bool());
}

TEST_F(TestParamsConsistency, ControlFrameExternal) {
  EXPECT_EQ(params_.control.frame.external,
            node_->get_parameter("control.frame.external").as_bool());
}

TEST_F(TestParamsConsistency, FixedWorldFrameExternal) {
  EXPECT_EQ(params_.fixed_world_frame.frame.external,
            node_->get_parameter("fixed_world_frame.frame.external").as_bool());
}

TEST_F(TestParamsConsistency, GravityCompensationFrameExternal) {
  EXPECT_EQ(
      params_.gravity_compensation.frame.external,
      node_->get_parameter("gravity_compensation.frame.external").as_bool());
}

TEST_F(TestParamsConsistency, GravityCompensationCogForceIsNan) {
  double gravity_comp_force = params_.gravity_compensation.CoG.force;
  double ros_param_force =
      node_->get_parameter("gravity_compensation.CoG.force").as_double();
  EXPECT_TRUE(std::isnan(gravity_comp_force));
  EXPECT_TRUE(std::isnan(ros_param_force));
}

// =========================================================================
// Dynamic Map Parameters Tests
// =========================================================================

TEST_F(TestParamsConsistency, MapJointsDofWeight) {
  for (const auto& joint : params_.joints) {
    for (const auto& dof : params_.dof_names) {
      const std::string param_name = fmt::format("{}.{}.weight", joint, dof);
      auto lib_value = params_.joints_map[joint].dof_names_map[dof].weight;
      auto ros_value = node_->get_parameter(param_name).as_double();
      EXPECT_DOUBLE_EQ(lib_value, ros_value)
          << fmt::format("Mismatch for {}: get_params()={}, get_parameter()={}",
                         param_name, lib_value, ros_value);
    }
  }
}

TEST_F(TestParamsConsistency, NestedDynamicMap) {
  for (const auto& joint : params_.joints) {
    for (const auto& dof : params_.dof_names) {
      const std::string param_name =
          fmt::format("nested_dynamic.{}.{}.nested", joint, dof);
      auto lib_value = params_.nested_dynamic.joints_map.at(joint)
                           .dof_names_map.at(dof)
                           .nested;
      auto ros_value = node_->get_parameter(param_name).as_double();
      EXPECT_DOUBLE_EQ(lib_value, ros_value)
          << fmt::format("Mismatch for {}: get_params()={}, get_parameter()={}",
                         param_name, lib_value, ros_value);
    }
  }
}

TEST_F(TestParamsConsistency, PidMapJointsP) {
  for (const auto& joint : params_.joints) {
    const std::string param_name = fmt::format("pid.{}.p", joint);
    auto lib_value = params_.pid.joints_map.at(joint).p;
    auto ros_value = node_->get_parameter(param_name).as_double();
    EXPECT_DOUBLE_EQ(lib_value, ros_value)
        << fmt::format("Mismatch for {}: get_params()={}, get_parameter()={}",
                       param_name, lib_value, ros_value);
  }
}

TEST_F(TestParamsConsistency, PidMapJointsI) {
  for (const auto& joint : params_.joints) {
    const std::string param_name = fmt::format("pid.{}.i", joint);
    auto lib_value = params_.pid.joints_map.at(joint).i;
    auto ros_value = node_->get_parameter(param_name).as_double();
    EXPECT_DOUBLE_EQ(lib_value, ros_value)
        << fmt::format("Mismatch for {}: get_params()={}, get_parameter()={}",
                       param_name, lib_value, ros_value);
  }
}

TEST_F(TestParamsConsistency, PidMapJointsD) {
  for (const auto& joint : params_.joints) {
    const std::string param_name = fmt::format("pid.{}.d", joint);
    auto lib_value = params_.pid.joints_map.at(joint).d;
    auto ros_value = node_->get_parameter(param_name).as_double();
    EXPECT_DOUBLE_EQ(lib_value, ros_value)
        << fmt::format("Mismatch for {}: get_params()={}, get_parameter()={}",
                       param_name, lib_value, ros_value);
  }
}

TEST_F(TestParamsConsistency, GainMapDofK) {
  for (const auto& dof : params_.dof_names) {
    const std::string param_name = fmt::format("gains.{}.k", dof);
    auto lib_value = params_.gains.dof_names_map.at(dof).k;
    auto ros_value = node_->get_parameter(param_name).as_double();
    EXPECT_DOUBLE_EQ(lib_value, ros_value)
        << fmt::format("Mismatch for {}: get_params()={}, get_parameter()={}",
                       param_name, lib_value, ros_value);
  }
}

// =========================================================================
// Consistency After set_parameters() Tests
// =========================================================================

TEST_F(TestParamsConsistency, UpdateInterpolationMode) {
  const std::string new_value = "linear";
  node_->set_parameters({rclcpp::Parameter("interpolation_mode", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_EQ(updated_params.interpolation_mode, new_value);
  EXPECT_EQ(updated_params.interpolation_mode,
            node_->get_parameter("interpolation_mode").as_string());
}

TEST_F(TestParamsConsistency, UpdateEnumControlMode) {
  node_->set_parameters({rclcpp::Parameter("control_mode", "effort")});
  auto updated_params = param_listener_->get_params();
  EXPECT_EQ(updated_params.control_mode,
            admittance_controller::Params::ControlMode::effort);
  EXPECT_EQ(to_string(updated_params.control_mode),
            node_->get_parameter("control_mode").as_string());
}

TEST_F(TestParamsConsistency, RejectEnumValueNotListed) {
  auto result =
      node_->set_parameters({rclcpp::Parameter("control_mode", "torque")});
  EXPECT_FALSE(result[0].successful);
  EXPECT_EQ(param_listener_->get_params().control_mode,
            admittance_controller::Params::ControlMode::position);
  EXPECT_EQ(node_->get_parameter("control_mode").as_string(), "position");
}

TEST_F(TestParamsConsistency, EnumReadFromDeclaredParameter) {
  // a new listener reads the value the node already holds
  node_->set_parameters({rclcpp::Parameter("control_mode", "velocity")});
  admittance_controller::ParamListener listener(
      node_->get_node_parameters_interface());
  EXPECT_EQ(listener.get_params().control_mode,
            admittance_controller::Params::ControlMode::velocity);
}

TEST_F(TestParamsConsistency, UpdateLtEqFifteen) {
  int64_t new_value = 10;
  node_->set_parameters({rclcpp::Parameter("lt_eq_fifteen", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_EQ(updated_params.lt_eq_fifteen, new_value);
  EXPECT_EQ(updated_params.lt_eq_fifteen,
            node_->get_parameter("lt_eq_fifteen").as_int());
}

TEST_F(TestParamsConsistency, UpdateMapJointDofWeight) {
  const auto& joint = params_.joints[0];
  const auto& dof = params_.dof_names[0];
  const std::string param_name = fmt::format("{}.{}.weight", joint, dof);
  double new_value = 2.5;
  node_->set_parameters({rclcpp::Parameter(param_name, new_value)});
  auto updated_params = param_listener_->get_params();
  auto lib_value =
      updated_params.joints_map.at(joint).dof_names_map.at(dof).weight;
  auto ros_value = node_->get_parameter(param_name).as_double();
  EXPECT_DOUBLE_EQ(lib_value, new_value);
  EXPECT_DOUBLE_EQ(lib_value, ros_value);
}

TEST_F(TestParamsConsistency, UpdateBoolEnableParameterUpdate) {
  bool new_value = false;
  node_->set_parameters({rclcpp::Parameter(
      "enable_parameter_update_without_reactivation", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_EQ(updated_params.enable_parameter_update_without_reactivation,
            new_value);
  EXPECT_EQ(updated_params.enable_parameter_update_without_reactivation,
            node_->get_parameter("enable_parameter_update_without_reactivation")
                .as_bool());
}

TEST_F(TestParamsConsistency, UpdateBoolAngleWraparound) {
  bool new_value = true;
  node_->set_parameters({rclcpp::Parameter("angle_wraparound", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_EQ(updated_params.angle_wraparound, new_value);
  EXPECT_EQ(updated_params.angle_wraparound,
            node_->get_parameter("angle_wraparound").as_bool());
}

TEST_F(TestParamsConsistency, UpdateBoolNestedFtSensorFrameExternal) {
  bool new_value = true;
  node_->set_parameters(
      {rclcpp::Parameter("ft_sensor.frame.external", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_EQ(updated_params.ft_sensor.frame.external, new_value);
  EXPECT_EQ(updated_params.ft_sensor.frame.external,
            node_->get_parameter("ft_sensor.frame.external").as_bool());
}

TEST_F(TestParamsConsistency, UpdateDoubleScientificNotationNum) {
  double new_value = 1.5e-4;
  node_->set_parameters(
      {rclcpp::Parameter("scientific_notation_num", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_DOUBLE_EQ(updated_params.scientific_notation_num, new_value);
  EXPECT_DOUBLE_EQ(updated_params.scientific_notation_num,
                   node_->get_parameter("scientific_notation_num").as_double());
}

TEST_F(TestParamsConsistency, UpdateDoublePidRate) {
  double new_value = 0.01;
  node_->set_parameters({rclcpp::Parameter("pid.rate", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_DOUBLE_EQ(updated_params.pid.rate, new_value);
  EXPECT_DOUBLE_EQ(updated_params.pid.rate,
                   node_->get_parameter("pid.rate").as_double());
}

TEST_F(TestParamsConsistency, UpdateDoubleArrayFixedArray) {
  std::vector<double> new_value{9.9, 8.8, 7.7, 6.6, 5.5};
  node_->set_parameters({rclcpp::Parameter("fixed_array", new_value)});
  auto updated_params = param_listener_->get_params();
  auto params_vec = rsl::to_vector(updated_params.fixed_array);
  EXPECT_THAT(params_vec, ::testing::ElementsAreArray(new_value));
  auto param_vec = node_->get_parameter("fixed_array").as_double_array();
  EXPECT_THAT(params_vec, ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, UpdateBoolArrayFixedArray) {
  std::vector<bool> new_value{false, true};
  node_->set_parameters({rclcpp::Parameter("fixed_bool_array", new_value)});
  auto updated_params = param_listener_->get_params();
  auto params_vec = rsl::to_vector(updated_params.fixed_bool_array);
  EXPECT_THAT(params_vec, ::testing::ElementsAreArray(new_value));
  auto param_vec = node_->get_parameter("fixed_bool_array").as_bool_array();
  EXPECT_THAT(params_vec, ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, RejectBoolArrayAboveFixedSize) {
  std::vector<bool> too_long(6, true);
  auto result =
      node_->set_parameters({rclcpp::Parameter("fixed_bool_array", too_long)});
  EXPECT_FALSE(result[0].successful);
}

TEST_F(TestParamsConsistency, UpdateDoubleArrayAdmittanceMass) {
  std::vector<double> new_value{1.0, 2.0, 3.0, 4.0, 5.0, 6.0};
  node_->set_parameters({rclcpp::Parameter("admittance.mass", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_THAT(updated_params.admittance.mass,
              ::testing::ElementsAreArray(new_value));
  auto param_vec = node_->get_parameter("admittance.mass").as_double_array();
  EXPECT_THAT(updated_params.admittance.mass,
              ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, UpdateBoolArrayAdmittanceSelectedAxes) {
  std::vector<bool> new_value{true, false, true, false, true, false};
  node_->set_parameters(
      {rclcpp::Parameter("admittance.selected_axes", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_THAT(updated_params.admittance.selected_axes,
              ::testing::ElementsAreArray(new_value));
  auto param_vec =
      node_->get_parameter("admittance.selected_axes").as_bool_array();
  EXPECT_THAT(updated_params.admittance.selected_axes,
              ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, UpdateStringArraySubsetSelection) {
  std::vector<std::string> new_value{"A"};
  node_->set_parameters({rclcpp::Parameter("subset_selection", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_THAT(updated_params.subset_selection,
              ::testing::ElementsAreArray(new_value));
  auto param_vec = node_->get_parameter("subset_selection").as_string_array();
  EXPECT_THAT(updated_params.subset_selection,
              ::testing::ElementsAreArray(param_vec));
}

TEST_F(TestParamsConsistency, UpdateIntGtFifteen) {
  int64_t new_value = 42;
  node_->set_parameters({rclcpp::Parameter("gt_fifteen", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_EQ(updated_params.gt_fifteen, new_value);
  EXPECT_EQ(updated_params.gt_fifteen,
            node_->get_parameter("gt_fifteen").as_int());
}

TEST_F(TestParamsConsistency, UpdateIntHoverOverride) {
  int64_t new_value = 0;
  node_->set_parameters({rclcpp::Parameter("hover_override", new_value)});
  auto updated_params = param_listener_->get_params();
  EXPECT_EQ(updated_params.hover_override, new_value);
  EXPECT_EQ(updated_params.hover_override,
            node_->get_parameter("hover_override").as_int());
}

TEST_F(TestParamsConsistency, UpdateMapPidJointP) {
  const auto& joint = params_.joints[0];
  const std::string param_name = fmt::format("pid.{}.p", joint);
  double new_value = 5.0;
  node_->set_parameters({rclcpp::Parameter(param_name, new_value)});
  auto updated_params = param_listener_->get_params();
  auto lib_value = updated_params.pid.joints_map.at(joint).p;
  auto ros_value = node_->get_parameter(param_name).as_double();
  EXPECT_DOUBLE_EQ(lib_value, new_value);
  EXPECT_DOUBLE_EQ(lib_value, ros_value);
}

TEST_F(TestParamsConsistency, UpdateMapGainsDofK) {
  const auto& dof = params_.dof_names[0];
  const std::string param_name = fmt::format("gains.{}.k", dof);
  double new_value = 10.0;
  node_->set_parameters({rclcpp::Parameter(param_name, new_value)});
  auto updated_params = param_listener_->get_params();
  auto lib_value = updated_params.gains.dof_names_map.at(dof).k;
  auto ros_value = node_->get_parameter(param_name).as_double();
  EXPECT_DOUBLE_EQ(lib_value, new_value);
  EXPECT_DOUBLE_EQ(lib_value, ros_value);
}

TEST_F(TestParamsConsistency, UpdateNestedDynamicMap) {
  const auto& joint = params_.joints[0];
  const auto& dof = params_.dof_names[0];
  const std::string param_name =
      fmt::format("nested_dynamic.{}.{}.nested", joint, dof);
  double new_value = 3.14;
  node_->set_parameters({rclcpp::Parameter(param_name, new_value)});
  auto updated_params = param_listener_->get_params();
  auto lib_value = updated_params.nested_dynamic.joints_map.at(joint)
                       .dof_names_map.at(dof)
                       .nested;
  auto ros_value = node_->get_parameter(param_name).as_double();
  EXPECT_DOUBLE_EQ(lib_value, new_value);
  EXPECT_DOUBLE_EQ(lib_value, ros_value);
}

TEST_F(TestParamsConsistency, ParamsDoNotShareState) {
  auto params1 = param_listener_->get_params();
  params1.pid.rate = 1.0;
  auto params2 = param_listener_->get_params();
  params2.pid.rate = 2.0;
  EXPECT_NE(params1.pid.rate, params2.pid.rate);
  node_->set_parameters({rclcpp::Parameter("pid.rate", 3.0)});
  params2 = param_listener_->get_params();
  EXPECT_NE(params1.pid.rate, params2.pid.rate);
}

TEST_F(TestParamsConsistency, MapsDoNotShareState) {
  node_->set_parameters({
      rclcpp::Parameter("nested_map_struct.A.nested_struct.nested_struct_field",
                        "valueA"),
      rclcpp::Parameter("nested_map_struct.B.nested_struct.nested_struct_field",
                        "valueB"),
  });
  auto params = param_listener_->get_params();
  EXPECT_NE(params.nested_map_struct.nested_map_struct_entries_map.at("A")
                .nested_struct.nested_struct_field,
            params.nested_map_struct.nested_map_struct_entries_map.at("B")
                .nested_struct.nested_struct_field);
}

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
