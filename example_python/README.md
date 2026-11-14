# Example:

## Build the node

```
 mkdir colcon_ws
 mkdir colcon_ws/src
 cd colcon_ws/src
 git clone https://github.com/picknikrobotics/generate_parameter_library.git
 cd ..
 colcon build
```

## Run the Python node

```
source install/setup.bash
ros2 run generate_parameter_module_example test_node --ros-args --params-file src/generate_parameter_library/example_python/config/implementation.yaml
```

You should see an output like this:
`[INFO] [1656018676.015816509] [admittance_controller]: Initial control frame parameter is: 'ee_link'`


## ROS 2 CLI

Run the following:

`ros2 param list`

You should see:

```
/admittance_controller:
  acceleration_limits
  admittance.damping_ratio
  admittance.mass
  admittance.selected_axes
  admittance.stiffness
  angle_wraparound
  chainable_command_interfaces
  command_interfaces
  control.frame.external
  control.frame.id
  dof_names
  elbow_joint.rz.limit
  elbow_joint.rz.weight
  elbow_joint.x.limit
  elbow_joint.x.weight
  elbow_joint.y.limit
  elbow_joint.y.weight
  enable_parameter_update_without_reactivation
  fixed_array
  fixed_string
  fixed_string_array
  fixed_string_array_no_default
  fixed_string_no_default
  fixed_world_frame.frame.external
  fixed_world_frame.frame.id
  ft_sensor.filter_coefficient
  ft_sensor.frame.external
  ft_sensor.frame.id
  ft_sensor.name
  gains.rz.k
  gains.x.k
  gains.y.k
  gravity_compensation.CoG.force
  gravity_compensation.CoG.pos
  gravity_compensation.frame.external
  gravity_compensation.frame.id
  gt_fifteen
  gt_fifteen_lt_eq_twenty
  gt_fifteen_lt_twenty
  hover_override
  interpolation_mode
  joints
  kinematics.alpha
  kinematics.base
  kinematics.group_name
  kinematics.plugin_name
  kinematics.plugin_package
  kinematics.tip
  lt_eq_fifteen
  nested_dynamic.elbow_joint.rz.elbow_joint.rz.nested_deep
  nested_dynamic.elbow_joint.rz.elbow_joint.x.nested_deep
  nested_dynamic.elbow_joint.rz.elbow_joint.y.nested_deep
  nested_dynamic.elbow_joint.rz.nested
  nested_dynamic.elbow_joint.rz.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.elbow_joint.rz.shoulder_lift_joint.x.nested_deep
  nested_dynamic.elbow_joint.rz.shoulder_lift_joint.y.nested_deep
  nested_dynamic.elbow_joint.rz.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.elbow_joint.rz.shoulder_pan_joint.x.nested_deep
  nested_dynamic.elbow_joint.rz.shoulder_pan_joint.y.nested_deep
  nested_dynamic.elbow_joint.rz.wrist_1_joint.rz.nested_deep
  nested_dynamic.elbow_joint.rz.wrist_1_joint.x.nested_deep
  nested_dynamic.elbow_joint.rz.wrist_1_joint.y.nested_deep
  nested_dynamic.elbow_joint.rz.wrist_2_joint.rz.nested_deep
  nested_dynamic.elbow_joint.rz.wrist_2_joint.x.nested_deep
  nested_dynamic.elbow_joint.rz.wrist_2_joint.y.nested_deep
  nested_dynamic.elbow_joint.rz.wrist_3_joint.rz.nested_deep
  nested_dynamic.elbow_joint.rz.wrist_3_joint.x.nested_deep
  nested_dynamic.elbow_joint.rz.wrist_3_joint.y.nested_deep
  nested_dynamic.elbow_joint.x.elbow_joint.rz.nested_deep
  nested_dynamic.elbow_joint.x.elbow_joint.x.nested_deep
  nested_dynamic.elbow_joint.x.elbow_joint.y.nested_deep
  nested_dynamic.elbow_joint.x.nested
  nested_dynamic.elbow_joint.x.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.elbow_joint.x.shoulder_lift_joint.x.nested_deep
  nested_dynamic.elbow_joint.x.shoulder_lift_joint.y.nested_deep
  nested_dynamic.elbow_joint.x.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.elbow_joint.x.shoulder_pan_joint.x.nested_deep
  nested_dynamic.elbow_joint.x.shoulder_pan_joint.y.nested_deep
  nested_dynamic.elbow_joint.x.wrist_1_joint.rz.nested_deep
  nested_dynamic.elbow_joint.x.wrist_1_joint.x.nested_deep
  nested_dynamic.elbow_joint.x.wrist_1_joint.y.nested_deep
  nested_dynamic.elbow_joint.x.wrist_2_joint.rz.nested_deep
  nested_dynamic.elbow_joint.x.wrist_2_joint.x.nested_deep
  nested_dynamic.elbow_joint.x.wrist_2_joint.y.nested_deep
  nested_dynamic.elbow_joint.x.wrist_3_joint.rz.nested_deep
  nested_dynamic.elbow_joint.x.wrist_3_joint.x.nested_deep
  nested_dynamic.elbow_joint.x.wrist_3_joint.y.nested_deep
  nested_dynamic.elbow_joint.y.elbow_joint.rz.nested_deep
  nested_dynamic.elbow_joint.y.elbow_joint.x.nested_deep
  nested_dynamic.elbow_joint.y.elbow_joint.y.nested_deep
  nested_dynamic.elbow_joint.y.nested
  nested_dynamic.elbow_joint.y.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.elbow_joint.y.shoulder_lift_joint.x.nested_deep
  nested_dynamic.elbow_joint.y.shoulder_lift_joint.y.nested_deep
  nested_dynamic.elbow_joint.y.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.elbow_joint.y.shoulder_pan_joint.x.nested_deep
  nested_dynamic.elbow_joint.y.shoulder_pan_joint.y.nested_deep
  nested_dynamic.elbow_joint.y.wrist_1_joint.rz.nested_deep
  nested_dynamic.elbow_joint.y.wrist_1_joint.x.nested_deep
  nested_dynamic.elbow_joint.y.wrist_1_joint.y.nested_deep
  nested_dynamic.elbow_joint.y.wrist_2_joint.rz.nested_deep
  nested_dynamic.elbow_joint.y.wrist_2_joint.x.nested_deep
  nested_dynamic.elbow_joint.y.wrist_2_joint.y.nested_deep
  nested_dynamic.elbow_joint.y.wrist_3_joint.rz.nested_deep
  nested_dynamic.elbow_joint.y.wrist_3_joint.x.nested_deep
  nested_dynamic.elbow_joint.y.wrist_3_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.elbow_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.elbow_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.elbow_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.nested
  nested_dynamic.shoulder_lift_joint.rz.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.shoulder_lift_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.shoulder_lift_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.shoulder_pan_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.shoulder_pan_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.wrist_1_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.wrist_1_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.wrist_1_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.wrist_2_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.wrist_2_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.wrist_2_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.wrist_3_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.wrist_3_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.rz.wrist_3_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.x.elbow_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.x.elbow_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.x.elbow_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.x.nested
  nested_dynamic.shoulder_lift_joint.x.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.x.shoulder_lift_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.x.shoulder_lift_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.x.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.x.shoulder_pan_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.x.shoulder_pan_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.x.wrist_1_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.x.wrist_1_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.x.wrist_1_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.x.wrist_2_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.x.wrist_2_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.x.wrist_2_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.x.wrist_3_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.x.wrist_3_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.x.wrist_3_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.y.elbow_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.y.elbow_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.y.elbow_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.y.nested
  nested_dynamic.shoulder_lift_joint.y.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.y.shoulder_lift_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.y.shoulder_lift_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.y.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.y.shoulder_pan_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.y.shoulder_pan_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.y.wrist_1_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.y.wrist_1_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.y.wrist_1_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.y.wrist_2_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.y.wrist_2_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.y.wrist_2_joint.y.nested_deep
  nested_dynamic.shoulder_lift_joint.y.wrist_3_joint.rz.nested_deep
  nested_dynamic.shoulder_lift_joint.y.wrist_3_joint.x.nested_deep
  nested_dynamic.shoulder_lift_joint.y.wrist_3_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.elbow_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.elbow_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.elbow_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.nested
  nested_dynamic.shoulder_pan_joint.rz.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.shoulder_lift_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.shoulder_lift_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.shoulder_pan_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.shoulder_pan_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.wrist_1_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.wrist_1_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.wrist_1_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.wrist_2_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.wrist_2_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.wrist_2_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.wrist_3_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.wrist_3_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.rz.wrist_3_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.x.elbow_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.x.elbow_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.x.elbow_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.x.nested
  nested_dynamic.shoulder_pan_joint.x.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.x.shoulder_lift_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.x.shoulder_lift_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.x.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.x.shoulder_pan_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.x.shoulder_pan_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.x.wrist_1_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.x.wrist_1_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.x.wrist_1_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.x.wrist_2_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.x.wrist_2_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.x.wrist_2_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.x.wrist_3_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.x.wrist_3_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.x.wrist_3_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.y.elbow_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.y.elbow_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.y.elbow_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.y.nested
  nested_dynamic.shoulder_pan_joint.y.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.y.shoulder_lift_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.y.shoulder_lift_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.y.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.y.shoulder_pan_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.y.shoulder_pan_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.y.wrist_1_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.y.wrist_1_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.y.wrist_1_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.y.wrist_2_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.y.wrist_2_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.y.wrist_2_joint.y.nested_deep
  nested_dynamic.shoulder_pan_joint.y.wrist_3_joint.rz.nested_deep
  nested_dynamic.shoulder_pan_joint.y.wrist_3_joint.x.nested_deep
  nested_dynamic.shoulder_pan_joint.y.wrist_3_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.rz.elbow_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.rz.elbow_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.rz.elbow_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.rz.nested
  nested_dynamic.wrist_1_joint.rz.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.rz.shoulder_lift_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.rz.shoulder_lift_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.rz.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.rz.shoulder_pan_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.rz.shoulder_pan_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.rz.wrist_1_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.rz.wrist_1_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.rz.wrist_1_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.rz.wrist_2_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.rz.wrist_2_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.rz.wrist_2_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.rz.wrist_3_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.rz.wrist_3_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.rz.wrist_3_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.x.elbow_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.x.elbow_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.x.elbow_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.x.nested
  nested_dynamic.wrist_1_joint.x.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.x.shoulder_lift_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.x.shoulder_lift_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.x.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.x.shoulder_pan_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.x.shoulder_pan_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.x.wrist_1_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.x.wrist_1_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.x.wrist_1_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.x.wrist_2_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.x.wrist_2_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.x.wrist_2_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.x.wrist_3_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.x.wrist_3_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.x.wrist_3_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.y.elbow_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.y.elbow_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.y.elbow_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.y.nested
  nested_dynamic.wrist_1_joint.y.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.y.shoulder_lift_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.y.shoulder_lift_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.y.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.y.shoulder_pan_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.y.shoulder_pan_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.y.wrist_1_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.y.wrist_1_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.y.wrist_1_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.y.wrist_2_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.y.wrist_2_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.y.wrist_2_joint.y.nested_deep
  nested_dynamic.wrist_1_joint.y.wrist_3_joint.rz.nested_deep
  nested_dynamic.wrist_1_joint.y.wrist_3_joint.x.nested_deep
  nested_dynamic.wrist_1_joint.y.wrist_3_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.rz.elbow_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.rz.elbow_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.rz.elbow_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.rz.nested
  nested_dynamic.wrist_2_joint.rz.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.rz.shoulder_lift_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.rz.shoulder_lift_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.rz.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.rz.shoulder_pan_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.rz.shoulder_pan_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.rz.wrist_1_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.rz.wrist_1_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.rz.wrist_1_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.rz.wrist_2_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.rz.wrist_2_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.rz.wrist_2_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.rz.wrist_3_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.rz.wrist_3_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.rz.wrist_3_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.x.elbow_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.x.elbow_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.x.elbow_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.x.nested
  nested_dynamic.wrist_2_joint.x.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.x.shoulder_lift_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.x.shoulder_lift_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.x.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.x.shoulder_pan_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.x.shoulder_pan_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.x.wrist_1_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.x.wrist_1_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.x.wrist_1_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.x.wrist_2_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.x.wrist_2_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.x.wrist_2_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.x.wrist_3_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.x.wrist_3_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.x.wrist_3_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.y.elbow_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.y.elbow_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.y.elbow_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.y.nested
  nested_dynamic.wrist_2_joint.y.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.y.shoulder_lift_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.y.shoulder_lift_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.y.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.y.shoulder_pan_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.y.shoulder_pan_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.y.wrist_1_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.y.wrist_1_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.y.wrist_1_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.y.wrist_2_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.y.wrist_2_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.y.wrist_2_joint.y.nested_deep
  nested_dynamic.wrist_2_joint.y.wrist_3_joint.rz.nested_deep
  nested_dynamic.wrist_2_joint.y.wrist_3_joint.x.nested_deep
  nested_dynamic.wrist_2_joint.y.wrist_3_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.rz.elbow_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.rz.elbow_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.rz.elbow_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.rz.nested
  nested_dynamic.wrist_3_joint.rz.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.rz.shoulder_lift_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.rz.shoulder_lift_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.rz.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.rz.shoulder_pan_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.rz.shoulder_pan_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.rz.wrist_1_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.rz.wrist_1_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.rz.wrist_1_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.rz.wrist_2_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.rz.wrist_2_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.rz.wrist_2_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.rz.wrist_3_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.rz.wrist_3_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.rz.wrist_3_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.x.elbow_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.x.elbow_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.x.elbow_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.x.nested
  nested_dynamic.wrist_3_joint.x.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.x.shoulder_lift_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.x.shoulder_lift_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.x.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.x.shoulder_pan_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.x.shoulder_pan_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.x.wrist_1_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.x.wrist_1_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.x.wrist_1_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.x.wrist_2_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.x.wrist_2_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.x.wrist_2_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.x.wrist_3_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.x.wrist_3_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.x.wrist_3_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.y.elbow_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.y.elbow_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.y.elbow_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.y.nested
  nested_dynamic.wrist_3_joint.y.shoulder_lift_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.y.shoulder_lift_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.y.shoulder_lift_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.y.shoulder_pan_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.y.shoulder_pan_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.y.shoulder_pan_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.y.wrist_1_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.y.wrist_1_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.y.wrist_1_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.y.wrist_2_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.y.wrist_2_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.y.wrist_2_joint.y.nested_deep
  nested_dynamic.wrist_3_joint.y.wrist_3_joint.rz.nested_deep
  nested_dynamic.wrist_3_joint.y.wrist_3_joint.x.nested_deep
  nested_dynamic.wrist_3_joint.y.wrist_3_joint.y.nested_deep
  nested_map.entries
  nested_map.entry1.value
  nested_map.entry2.value
  one_number
  open_loop_control
  pid.elbow_joint.d
  pid.elbow_joint.i
  pid.elbow_joint.p
  pid.rate
  pid.shoulder_lift_joint.d
  pid.shoulder_lift_joint.i
  pid.shoulder_lift_joint.p
  pid.shoulder_pan_joint.d
  pid.shoulder_pan_joint.i
  pid.shoulder_pan_joint.p
  pid.wrist_1_joint.d
  pid.wrist_1_joint.i
  pid.wrist_1_joint.p
  pid.wrist_2_joint.d
  pid.wrist_2_joint.i
  pid.wrist_2_joint.p
  pid.wrist_3_joint.d
  pid.wrist_3_joint.i
  pid.wrist_3_joint.p
  scientific_notation_num
  shoulder_lift_joint.rz.limit
  shoulder_lift_joint.rz.weight
  shoulder_lift_joint.x.limit
  shoulder_lift_joint.x.weight
  shoulder_lift_joint.y.limit
  shoulder_lift_joint.y.weight
  shoulder_pan_joint.rz.limit
  shoulder_pan_joint.rz.weight
  shoulder_pan_joint.x.limit
  shoulder_pan_joint.x.weight
  shoulder_pan_joint.y.limit
  shoulder_pan_joint.y.weight
  start_type_description_service
  state_interfaces
  subset_selection
  three_numbers
  three_numbers_of_five
  use_feedforward_commanded_input
  use_sim_time
  wrist_1_joint.rz.limit
  wrist_1_joint.rz.weight
  wrist_1_joint.x.limit
  wrist_1_joint.x.weight
  wrist_1_joint.y.limit
  wrist_1_joint.y.weight
  wrist_2_joint.rz.limit
  wrist_2_joint.rz.weight
  wrist_2_joint.x.limit
  wrist_2_joint.x.weight
  wrist_2_joint.y.limit
  wrist_2_joint.y.weight
  wrist_3_joint.rz.limit
  wrist_3_joint.rz.weight
  wrist_3_joint.x.limit
  wrist_3_joint.x.weight
  wrist_3_joint.y.limit
  wrist_3_joint.y.weight
  ```

All parameter are automatically declared and callbacks are setup by default. You can set a parameter by typing:

`ros2 param set /admittance_controller control.frame.id new_frame`

You should see:

`[INFO] [1656019001.515820371] [admittance_controller]: New control frame parameter is: 'new_frame'`

Congratulations, you updated the parameter!

If you try to set a parameter that is read only, you will get an error. Running the following

`ros2 param set /admittance_controller command_interfaces ["velocity"]`

will result in the error

`Setting parameter failed: Trying to set a read-only parameter: command_interfaces.`

Running the following

`ros2 param describe /admittance_controller admittance.damping_ratio`

will show a parameter's description

 ```
 Parameter name: admittance.damping_ratio
  Type: double array
  Description: specifies damping ratio values for x, y, z, rx, ry, and rz used in the admittance calculation. The values are calculated as damping can be used instead: zeta = D / (2 * sqrt( M * S ))
  Constraints:
    Min value: 0.1
    Max value: 10.0
```

If you try to set a value out of the specified bounds,

`ros2 param set /admittance_controller admittance.damping_ratio [-10.0,-10.0,-10.0,-10.0,-10.0,-10.0]`

you will get the error

`Setting parameter failed: Value -10.0 in parameter 'admittance.damping_ratio' must be within bounds [0.1, 10.0]`

If you try to set a vector parameter with the wrong length,

`ros2 param set /admittance_controller admittance.damping_ratio [1.0,1.0,1.0]`

you will get the error

`Setting parameter failed: Length of parameter 'admittance.damping_ratio' is '3' but must be equal to 6`

If you try to load a yaml file with missing required parameters

`ros2 run generate_parameter_module_example test_node --ros-args --params-file src/generate_parameter_library/example_python/config/missing_required.yaml`

you will get the error

```
Traceback (most recent call last):
[...]
rclpy.exceptions.ParameterUninitializedException: The parameter 'fixed_string_no_default' is not initialized
[ros2run]: Process exited with failure 1
```
