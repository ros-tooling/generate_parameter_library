#!/usr/bin/env python3

# Copyright 2026 Mat198
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Tests that verify consistency between get_params() (library internal state)
and node.get_parameter() (ROS2 parameter server) for admittance_controller.

After ParamListener.__init__() calls declare_params(), all parameters (static
and dynamic map entries) are declared in the ROS2 node and read back via
get_parameter(), then stored in params_ via update_internal_params(). This
test verifies both sources remain in sync under the example configuration
values and after updates via set_parameters().
"""

import importlib
import math
import os
import unittest

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

from generate_parameter_module_example.admittance_parameters import (
    admittance_controller,
)


class TestParamsConsistency(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the example configuration file instead of hardcoding parameter
        # values: it provides every required parameter (those declared with
        # type-only and no default_value). Without these, declare_params()
        # raises ParameterUninitializedException when calling get_parameter()
        # on them after declare_parameter(type_only).
        config = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            'config',
            'implementation.yaml',
        )
        rclpy.init(args=['--ros-args', '--params-file', config])

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.node = Node(
            'admittance_controller',
            automatically_declare_parameters_from_overrides=True,
        )
        self.listener = admittance_controller.ParamListener(self.node)
        self.params = self.listener.get_params()

    def tearDown(self):
        self.node.destroy_node()

    # -------------------------------------------------------------------------
    # Static / flat parameters
    # -------------------------------------------------------------------------

    def test_scientific_notation_num(self):
        self.assertAlmostEqual(
            self.params.scientific_notation_num,
            self.node.get_parameter('scientific_notation_num').value,
        )

    def test_interpolation_mode(self):
        self.assertEqual(
            self.params.interpolation_mode,
            self.node.get_parameter('interpolation_mode').value,
        )

    def test_subset_selection(self):
        self.assertEqual(
            list(self.params.subset_selection),
            list(self.node.get_parameter('subset_selection').value),
        )

    def test_joints(self):
        self.assertEqual(
            list(self.params.joints),
            list(self.node.get_parameter('joints').value),
        )

    def test_dof_names(self):
        self.assertEqual(
            list(self.params.dof_names),
            list(self.node.get_parameter('dof_names').value),
        )

    def test_fixed_string(self):
        self.assertEqual(
            self.params.fixed_string,
            self.node.get_parameter('fixed_string').value,
        )

    def test_fixed_array(self):
        self.assertEqual(
            list(self.params.fixed_array),
            list(self.node.get_parameter('fixed_array').value),
        )

    def test_enable_parameter_update_without_reactivation(self):
        self.assertEqual(
            self.params.enable_parameter_update_without_reactivation,
            self.node.get_parameter(
                'enable_parameter_update_without_reactivation'
            ).value,
        )

    def test_use_feedforward_commanded_input(self):
        self.assertEqual(
            self.params.use_feedforward_commanded_input,
            self.node.get_parameter('use_feedforward_commanded_input').value,
        )

    def test_lt_eq_fifteen(self):
        self.assertEqual(
            self.params.lt_eq_fifteen,
            self.node.get_parameter('lt_eq_fifteen').value,
        )

    def test_gt_fifteen(self):
        self.assertEqual(
            self.params.gt_fifteen,
            self.node.get_parameter('gt_fifteen').value,
        )

    def test_one_number(self):
        self.assertEqual(
            self.params.one_number,
            self.node.get_parameter('one_number').value,
        )

    def test_three_numbers(self):
        self.assertEqual(
            list(self.params.three_numbers),
            list(self.node.get_parameter('three_numbers').value),
        )

    def test_three_numbers_of_five(self):
        self.assertEqual(
            list(self.params.three_numbers_of_five),
            list(self.node.get_parameter('three_numbers_of_five').value),
        )

    def test_hover_override(self):
        self.assertEqual(
            self.params.hover_override,
            self.node.get_parameter('hover_override').value,
        )

    def test_angle_wraparound(self):
        self.assertEqual(
            self.params.angle_wraparound,
            self.node.get_parameter('angle_wraparound').value,
        )

    def test_open_loop_control(self):
        self.assertEqual(
            self.params.open_loop_control,
            self.node.get_parameter('open_loop_control').value,
        )

    # -------------------------------------------------------------------------
    # Nested struct parameters
    # -------------------------------------------------------------------------

    def test_pid_rate(self):
        self.assertAlmostEqual(
            self.params.pid.rate,
            self.node.get_parameter('pid.rate').value,
        )

    def test_kinematics_alpha(self):
        self.assertAlmostEqual(
            self.params.kinematics.alpha,
            self.node.get_parameter('kinematics.alpha').value,
        )

    def test_ft_sensor_filter_coefficient(self):
        self.assertAlmostEqual(
            self.params.ft_sensor.filter_coefficient,
            self.node.get_parameter('ft_sensor.filter_coefficient').value,
        )

    def test_ft_sensor_frame_external(self):
        self.assertEqual(
            self.params.ft_sensor.frame.external,
            self.node.get_parameter('ft_sensor.frame.external').value,
        )

    def test_control_frame_external(self):
        self.assertEqual(
            self.params.control.frame.external,
            self.node.get_parameter('control.frame.external').value,
        )

    def test_fixed_world_frame_external(self):
        self.assertEqual(
            self.params.fixed_world_frame.frame.external,
            self.node.get_parameter('fixed_world_frame.frame.external').value,
        )

    def test_gravity_compensation_frame_external(self):
        self.assertEqual(
            self.params.gravity_compensation.frame.external,
            self.node.get_parameter('gravity_compensation.frame.external').value,
        )

    def test_gravity_compensation_cog_force_is_nan(self):
        # the example config file sets CoG.force to 23.0, so update the
        # parameter to NaN here to check that a NaN value survives the
        # round-trip through the parameter server
        self.node.set_parameters(
            [Parameter('gravity_compensation.CoG.force', value=float('nan'))]
        )
        updated_params = self.listener.get_params()
        self.assertTrue(math.isnan(updated_params.gravity_compensation.CoG.force))
        self.assertTrue(
            math.isnan(self.node.get_parameter('gravity_compensation.CoG.force').value)
        )

    # -------------------------------------------------------------------------
    # Dynamic map parameters
    # -------------------------------------------------------------------------

    def test_map_joints_dof_weight(self):
        for joint in self.params.joints:
            for dof in self.params.dof_names:
                param_name = f'{joint}.{dof}.weight'
                lib_value = self.params.get_entry(joint).get_entry(dof).weight
                ros_value = self.node.get_parameter(param_name).value
                self.assertAlmostEqual(
                    lib_value,
                    ros_value,
                    msg=f'Mismatch for {param_name}: get_params()={lib_value}, get_parameter()={ros_value}',
                )

    def test_nested_dynamic_map(self):
        for joint in self.params.joints:
            for dof in self.params.dof_names:
                param_name = f'nested_dynamic.{joint}.{dof}.nested'
                lib_value = (
                    self.params.nested_dynamic.get_entry(joint).get_entry(dof).nested
                )
                ros_value = self.node.get_parameter(param_name).value
                self.assertAlmostEqual(
                    lib_value,
                    ros_value,
                    msg=f'Mismatch for {param_name}: get_params()={lib_value}, get_parameter()={ros_value}',
                )

    def test_pid_map_joints_p(self):
        for joint in self.params.joints:
            param_name = f'pid.{joint}.p'
            lib_value = self.params.pid.get_entry(joint).p
            ros_value = self.node.get_parameter(param_name).value
            self.assertAlmostEqual(
                lib_value,
                ros_value,
                msg=f'Mismatch for {param_name}: get_params()={lib_value}, get_parameter()={ros_value}',
            )

    def test_pid_map_joints_i(self):
        for joint in self.params.joints:
            param_name = f'pid.{joint}.i'
            lib_value = self.params.pid.get_entry(joint).i
            ros_value = self.node.get_parameter(param_name).value
            self.assertAlmostEqual(
                lib_value,
                ros_value,
                msg=f'Mismatch for {param_name}: get_params()={lib_value}, get_parameter()={ros_value}',
            )

    def test_pid_map_joints_d(self):
        for joint in self.params.joints:
            param_name = f'pid.{joint}.d'
            lib_value = self.params.pid.get_entry(joint).d
            ros_value = self.node.get_parameter(param_name).value
            self.assertAlmostEqual(
                lib_value,
                ros_value,
                msg=f'Mismatch for {param_name}: get_params()={lib_value}, get_parameter()={ros_value}',
            )

    def test_gains_map_dof_k(self):
        for dof in self.params.dof_names:
            param_name = f'gains.{dof}.k'
            lib_value = self.params.gains.get_entry(dof).k
            ros_value = self.node.get_parameter(param_name).value
            self.assertAlmostEqual(
                lib_value,
                ros_value,
                msg=f'Mismatch for {param_name}: get_params()={lib_value}, get_parameter()={ros_value}',
            )

    # -------------------------------------------------------------------------
    # Consistency after set_parameters()
    # -------------------------------------------------------------------------

    def test_update_interpolation_mode(self):
        new_value = 'linear'
        self.node.set_parameters([Parameter('interpolation_mode', value=new_value)])
        updated_params = self.listener.get_params()
        self.assertEqual(updated_params.interpolation_mode, new_value)
        self.assertEqual(
            updated_params.interpolation_mode,
            self.node.get_parameter('interpolation_mode').value,
        )

    def test_update_lt_eq_fifteen(self):
        new_value = 10
        self.node.set_parameters([Parameter('lt_eq_fifteen', value=new_value)])
        updated_params = self.listener.get_params()
        self.assertEqual(updated_params.lt_eq_fifteen, new_value)
        self.assertEqual(
            updated_params.lt_eq_fifteen,
            self.node.get_parameter('lt_eq_fifteen').value,
        )

    def test_update_map_joint_dof_weight(self):
        joint = self.params.joints[0]
        dof = self.params.dof_names[0]
        param_name = f'{joint}.{dof}.weight'
        new_value = 2.5
        self.node.set_parameters([Parameter(param_name, value=new_value)])
        updated_params = self.listener.get_params()
        lib_value = updated_params.get_entry(joint).get_entry(dof).weight
        ros_value = self.node.get_parameter(param_name).value
        self.assertAlmostEqual(lib_value, new_value)
        self.assertAlmostEqual(lib_value, ros_value)

    def test_update_bool_enable_parameter_update(self):
        new_value = False
        self.node.set_parameters(
            [Parameter('enable_parameter_update_without_reactivation', value=new_value)]
        )
        updated_params = self.listener.get_params()
        self.assertEqual(
            updated_params.enable_parameter_update_without_reactivation, new_value
        )
        self.assertEqual(
            updated_params.enable_parameter_update_without_reactivation,
            self.node.get_parameter(
                'enable_parameter_update_without_reactivation'
            ).value,
        )

    def test_update_bool_angle_wraparound(self):
        new_value = True
        self.node.set_parameters([Parameter('angle_wraparound', value=new_value)])
        updated_params = self.listener.get_params()
        self.assertEqual(updated_params.angle_wraparound, new_value)
        self.assertEqual(
            updated_params.angle_wraparound,
            self.node.get_parameter('angle_wraparound').value,
        )

    def test_update_bool_nested_ft_sensor_frame_external(self):
        new_value = True
        self.node.set_parameters(
            [Parameter('ft_sensor.frame.external', value=new_value)]
        )
        updated_params = self.listener.get_params()
        self.assertEqual(updated_params.ft_sensor.frame.external, new_value)
        self.assertEqual(
            updated_params.ft_sensor.frame.external,
            self.node.get_parameter('ft_sensor.frame.external').value,
        )

    def test_update_double_scientific_notation_num(self):
        new_value = 1.5e-4
        self.node.set_parameters(
            [Parameter('scientific_notation_num', value=new_value)]
        )
        updated_params = self.listener.get_params()
        self.assertAlmostEqual(updated_params.scientific_notation_num, new_value)
        self.assertAlmostEqual(
            updated_params.scientific_notation_num,
            self.node.get_parameter('scientific_notation_num').value,
        )

    def test_update_double_pid_rate(self):
        new_value = 0.01
        self.node.set_parameters([Parameter('pid.rate', value=new_value)])
        updated_params = self.listener.get_params()
        self.assertAlmostEqual(updated_params.pid.rate, new_value)
        self.assertAlmostEqual(
            updated_params.pid.rate,
            self.node.get_parameter('pid.rate').value,
        )

    def test_update_double_array_fixed_array(self):
        new_value = [9.9, 8.8, 7.7, 6.6, 5.5]
        self.node.set_parameters([Parameter('fixed_array', value=new_value)])
        updated_params = self.listener.get_params()
        self.assertEqual(list(updated_params.fixed_array), new_value)
        self.assertEqual(
            list(updated_params.fixed_array),
            list(self.node.get_parameter('fixed_array').value),
        )

    def test_update_double_array_admittance_mass(self):
        new_value = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        self.node.set_parameters([Parameter('admittance.mass', value=new_value)])
        updated_params = self.listener.get_params()
        self.assertEqual(list(updated_params.admittance.mass), new_value)
        self.assertEqual(
            list(updated_params.admittance.mass),
            list(self.node.get_parameter('admittance.mass').value),
        )

    def test_update_bool_array_admittance_selected_axes(self):
        new_value = [True, False, True, False, True, False]
        self.node.set_parameters(
            [Parameter('admittance.selected_axes', value=new_value)]
        )
        updated_params = self.listener.get_params()
        self.assertEqual(list(updated_params.admittance.selected_axes), new_value)
        self.assertEqual(
            list(updated_params.admittance.selected_axes),
            list(self.node.get_parameter('admittance.selected_axes').value),
        )

    def test_update_string_array_subset_selection(self):
        new_value = ['A']
        self.node.set_parameters([Parameter('subset_selection', value=new_value)])
        updated_params = self.listener.get_params()
        self.assertEqual(list(updated_params.subset_selection), new_value)
        self.assertEqual(
            list(updated_params.subset_selection),
            list(self.node.get_parameter('subset_selection').value),
        )

    def test_update_int_gt_fifteen(self):
        new_value = 42
        self.node.set_parameters([Parameter('gt_fifteen', value=new_value)])
        updated_params = self.listener.get_params()
        self.assertEqual(updated_params.gt_fifteen, new_value)
        self.assertEqual(
            updated_params.gt_fifteen,
            self.node.get_parameter('gt_fifteen').value,
        )

    def test_update_int_hover_override(self):
        new_value = 0
        self.node.set_parameters([Parameter('hover_override', value=new_value)])
        updated_params = self.listener.get_params()
        self.assertEqual(updated_params.hover_override, new_value)
        self.assertEqual(
            updated_params.hover_override,
            self.node.get_parameter('hover_override').value,
        )

    def test_update_map_pid_joint_p(self):
        joint = self.params.joints[0]
        param_name = f'pid.{joint}.p'
        new_value = 5.0
        self.node.set_parameters([Parameter(param_name, value=new_value)])
        updated_params = self.listener.get_params()
        lib_value = updated_params.pid.get_entry(joint).p
        ros_value = self.node.get_parameter(param_name).value
        self.assertAlmostEqual(lib_value, new_value)
        self.assertAlmostEqual(lib_value, ros_value)

    def test_update_map_gains_dof_k(self):
        dof = self.params.dof_names[0]
        param_name = f'gains.{dof}.k'
        new_value = 10.0
        self.node.set_parameters([Parameter(param_name, value=new_value)])
        updated_params = self.listener.get_params()
        lib_value = updated_params.gains.get_entry(dof).k
        ros_value = self.node.get_parameter(param_name).value
        self.assertAlmostEqual(lib_value, new_value)
        self.assertAlmostEqual(lib_value, ros_value)

    def test_update_nested_dynamic_map(self):
        joint = self.params.joints[0]
        dof = self.params.dof_names[0]
        param_name = f'nested_dynamic.{joint}.{dof}.nested'
        new_value = 3.14
        self.node.set_parameters([Parameter(param_name, value=new_value)])
        updated_params = self.listener.get_params()
        lib_value = updated_params.nested_dynamic.get_entry(joint).get_entry(dof).nested
        ros_value = self.node.get_parameter(param_name).value
        self.assertAlmostEqual(lib_value, new_value)
        self.assertAlmostEqual(lib_value, ros_value)

    def test_params_do_not_share_state(self):
        params1 = self.listener.get_params()
        params1.pid.rate = 1.0
        params2 = self.listener.get_params()
        params2.pid.rate = 2.0
        self.assertNotEqual(params1.pid.rate, params2.pid.rate)
        self.node.set_parameters([Parameter('pid.rate', value='3.0')])
        params2 = self.listener.get_params()
        self.assertNotEqual(params1.pid.rate, params2.pid.rate)

    def test_maps_do_not_share_state(self):
        self.node.set_parameters(
            [
                Parameter(
                    'nested_map_struct.A.nested_struct.nested_struct_field',
                    value='valueA',
                ),
                Parameter(
                    'nested_map_struct.B.nested_struct.nested_struct_field',
                    value='valueB',
                ),
            ]
        )
        params = self.listener.get_params()
        self.assertNotEqual(
            params.nested_map_struct.get_entry('A').nested_struct.nested_struct_field,
            params.nested_map_struct.get_entry('B').nested_struct.nested_struct_field,
        )

    def test_update_unrelated_param_does_not_mark_params_as_old(self):
        params_before = self.listener.get_params()
        self.node.declare_parameter('some_other_parameter', 42)
        self.node.set_parameters([Parameter('some_other_parameter', value=43)])
        self.assertFalse(self.listener.is_old(params_before))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
