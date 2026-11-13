# generate_parameter_library
Generate C++ or Python code for ROS 2 parameter declaration, getting, and validation using declarative YAML.
The generated library contains a C++ struct with specified parameters.
Additionally, dynamic parameters and custom validation are made easy.

## TOC
- [Killer Features](#killer-features)
- [Basic Usage](#basic-usage)
- [Detailed Documentation](#detailed-documentation)
- [FAQ](#faq)
- [Build status](#build-status)

## Killer Features
* Declarative YAML syntax for ROS 2 Parameters converted into C++ or Python struct
* Declaring, Getting, Validating, and Updating handled by generated code
* Dynamic ROS 2 Parameters made easy
* Custom user-specified validator functions
* Automatically create documentation of parameters

## Basic Usage
1. [Create YAML parameter codegen file](#create-yaml-parameter-codegen-file)
2. [Add parameter library generation to project](#add-parameter-library-generation-to-project)
3. [Use generated struct in project source code](#use-generated-struct-in-project-source-code)

### Create yaml parameter codegen file
Write a yaml file to declare your parameters and their attributes.

**src/turtlesim_parameters.yaml**
```yaml
turtlesim:
  background:
    r:
      type: int
      default_value: 0
      description: "Red color value for the background, 8-bit"
      validation:
        bounds<>: [0, 255]
    g:
      type: int
      default_value: 0
      description: "Green color value for the background, 8-bit"
      validation:
        bounds<>: [0, 255]
    b:
      type: int
      default_value: 0
      description: "Blue color value for the background, 8-bit"
      validation:
        bounds<>: [0, 255]
```

### Add parameter library generation to project

**package.xml**
```xml
<depend>generate_parameter_library</depend>
```

**CMakeLists.txt**
```cmake
find_package(generate_parameter_library REQUIRED)

generate_parameter_library(
  turtlesim_parameters # cmake target name for the parameter library
  src/turtlesim_parameters.yaml # path to input yaml file
)

add_executable(minimal_node src/turtlesim.cpp)
target_link_libraries(minimal_node PRIVATE
  rclcpp::rclcpp
  turtlesim_parameters
)

install(TARGETS minimal_node turtlesim_parameters
  EXPORT ${PROJECT_NAME}Targets)
ament_export_targets(${PROJECT_NAME}Targets HAS_LIBRARY_TARGET)
```

**setup.py**
```python
from setuptools import setup
from generate_parameter_library_py.setup_helper import parameter_cmdclass

setup(
  name="turtlesim",
  packages=["turtlesim"],
  cmdclass=parameter_cmdclass(
    "turtlesim_parameters", # python module name for parameter library
    "turtlesim/turtlesim_parameters.yaml", # path to input yaml file
  ),
)
```

The module is generated during the build, so it installs with the package, including with `--symlink-install` and other editable installs.
For several modules, pass a list:

```python
cmdclass=parameter_cmdclass(modules=[
  {"module_name": "turtlesim_parameters", "yaml_file": "turtlesim/turtlesim_parameters.yaml"},
  {"module_name": "pen_parameters", "yaml_file": "config/pen_parameters.yaml", "package": "turtlesim"},
]),
```

If the package has its own `__init__.py`, `colcon test` imports the source tree before the installed package, so tests must drop the package's source directory from `sys.path`; see [example_python/test/conftest.py](example_python/test/conftest.py).
The older `generate_parameter_module()` call in `setup.py` still works.

For a Python package built with `ament_cmake_python`, use `generate_parameter_module()`
in `CMakeLists.txt` and install the Python package with `ament_python_install_package()`:

```cmake
cmake_minimum_required(VERSION 3.16)
project(turtlesim)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(generate_parameter_library REQUIRED)

generate_parameter_module(turtlesim_parameters
  src/turtlesim_parameters.yaml
  # Optional third argument: turtlesim.custom_validation
)

ament_python_install_package(${PROJECT_NAME})
ament_package()
```

This example expects a Python package directory named `turtlesim` alongside
`CMakeLists.txt`. In addition to the `generate_parameter_library` dependency above,
declare `ament_cmake_python` as a build tool dependency in `package.xml` and use
`ament_cmake` as the package's build type:

```xml
<buildtool_depend>ament_cmake_python</buildtool_depend>
<export>
  <build_type>ament_cmake</build_type>
</export>
```

See [example_cmake_python](example_cmake_python) for the complete package.

### Use generated struct in project source code

**src/turtlesim.cpp**
```c++
#include <rclcpp/rclcpp.hpp>
#include <turtlesim/turtlesim_parameters.hpp>

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>("turtlesim");
  auto param_listener = std::make_shared<turtlesim::ParamListener>(node);
  auto params = param_listener->get_params();

  auto color = params.background;
  RCLCPP_INFO(node->get_logger(),
    "Background color (r,g,b): %d, %d, %d",
    color.r, color.g, color.b);

  return 0;
}
```

**turtlesim/turtlesim.py**
```python
import rclpy
from rclpy.node import Node
from turtlesim_pkg.turtlesim_parameters import turtlesim_parameters

def main(args=None):
  rclpy.init(args=args)
  node = Node("turtlesim")
  param_listener = turtlesim_parameters.ParamListener(node)
  params = param_listener.get_params()

  color = params.background
  node.get_logger().info(
    "Background color (r,g,b): %d, %d, %d" %
    color.r, color.g, color.b)
```

### Use example yaml files in tests
When using parameter library generation it can happen that there are issues when executing tests since parameters are not defined and the library defines them as mandatory.
To overcome this it is recommended to define example yaml files for tests and use them as follows:

```
find_package(ament_cmake_gtest REQUIRED)
add_rostest_with_parameters_gtest(test_turtlesim_parameters test/test_turtlesim_parameters.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test/example_turtlesim_parameters.yaml)
target_include_directories(test_turtlesim_parameters PRIVATE include)
target_link_libraries(test_turtlesim_parameters turtlesim_parameters)
ament_target_dependencies(test_turtlesim_parameters rclcpp)
```

when using `gtest`, or:

```
find_package(ament_cmake_gmock REQUIRED)
add_rostest_with_parameters_gmock(test_turtlesim_parameters test/test_turtlesim_parameters.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/test/example_turtlesim_parameters.yaml)
target_include_directories(test_turtlesim_parameters PRIVATE include)
target_link_libraries(test_turtlesim_parameters turtlesim_parameters)
ament_target_dependencies(test_turtlesim_parameters rclcpp)
```
when using `gmock` test library.

🤖 P.S. having this example yaml files will make your users very grateful because they will always have a working example of a configuration for your node.

## Detailed Documentation
* [Cpp namespace](#cpp-namespace)
* [Parameter definition](#parameter-definition)
* [Built-In Validators](#built-in-validators)
* [Custom validator functions](#custom-validator-functions)
* [Nested structures](#nested-structures)
* [Mapped parameters](#mapped-parameters)
* [Use generated struct in Cpp](#use-generated-struct-in-cpp)
* [Dynamic Parameters](#dynamic-parameters)
* [Parameter documentation](#parameter-documentation)
* [Example Project](#example-project)
* [Generated code output](#generated-code-output)
* [Generate markdown documentation](#generate-markdown-documentation)

### Cpp namespace
The root element of the YAML file determines the namespace used in the generated C++ code.
We use this to put the `Params` struct in the same namespace as your C++ code.

```yaml
cpp_namespace:
# additionally fields  ...
```

### Parameter definition
The YAML syntax can be thought of as a tree since it allows for arbitrary nesting of key-value pairs.
For clarity, the last non-nested value is referred to as a leaf.
A leaf represents a single parameter and has the following format.

```yaml
cpp_namespace:
  param_name:
    type: int
    default_value: 3
    read_only: true
    additional_constraints: "{ type: 'number', multipleOf: 3 }"
    description: "A read-only  integer parameter with a default value of 3"
    validation:
      # validation functions ...
```

A parameter is a YAML dictionary with the only required key being `type`.

| Field                  | Description                                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------------------------- |
| type                   | The type (string, double, etc) of the parameter.                                                               |
| default_value          | Value for the parameter if the user does not specify a value.                                                  |
| read_only              | Can only be set at launch and are not dynamic.                                                                 |
| description            | Displayed by `ros2 param describe`.                                                                            |
| validation             | Dictionary of validation functions and their parameters.                                                       |
| additional_constraints | Additional constraints that end up on the ParameterDescriptor but are not used for validation by this package. |

The types of parameters in ros2 map to C++ types.

| Parameter Type  | C++ Type                   |
| --------------- | -------------------------- |
| string          | `std::string`              |
| double          | `double`                   |
| int             | `int`                      |
| bool            | `bool`                     |
| string_array    | `std::vector<std::string>` |
| double_array    | `std::vector<double>`      |
| int_array       | `std::vector<int>`         |
| bool_array      | `std::vector<bool>`        |
| string_fixed_XX | `FixedSizeString<XX>`      |
| none            | NO CODE GENERATED          |

Fixed-size types are denoted with a suffix `_fixed_XX`, where `XX` is the desired size.
The corresponding C++ type is a data wrapper class for conveniently accessing the data.
Note that any fixed size type will automatically use a `size_lt` validator. Validators are explained in the next section.

The purpose of the `none` type is purely documentation, and won't generate any C++ code. See [Parameter documentation](#parameter-documentation) for details.

### Built-In Validators
Validators are C++ functions that take arguments represented by a key-value pair in yaml.
The key is the name of the function.
The value is an array of values that are passed in as parameters to the function.
If the function does not take any values you write `null` or `[]` to for the value.

```yaml
joint_trajectory_controller:
  command_interfaces:
    type: string_array
    description: "Names of command interfaces to claim"
    validation:
      size_gt<>: [0]
      unique<>: null
      subset_of<>: [["position", "velocity", "acceleration", "effort",]]
```

Above are validations for `command_interfaces` from `ros2_controllers`.
This will require this string_array to have these properties:

* There is at least one value in the array
* All values are unique
* Values are only in the set `["position", "velocity", "acceleration", "effort",]`

You will note that some validators have a suffix of `<>`, this tells the code generator to pass the C++ type of the parameter as a function template.
Some of these validators work only on value types, some on string types, and others on array types.
The built-in validator functions provided by this package are:

**Value validators**
| Function | Arguments           | Description                          |
| -------- | ------------------- | ------------------------------------ |
| bounds<> | [lower, upper]      | Bounds checking (inclusive)          |
| lt<>     | [value]             | parameter < value                    |
| gt<>     | [value]             | parameter > value                    |
| lt_eq<>  | [value]             | parameter <= value                   |
| gt_eq<>  | [value]             | parameter >= value                   |
| one_of<> | [[val1, val2, ...]] | Value is one of the specified values |

Note: `lt<>`, `gt<>`, `lt_eq<>`, or `gt_eq<>` cannot be used together with `bounds<>`.

**String validators**
| Function     | Arguments           | Description                                    |
| ------------ | ------------------- | ---------------------------------------------- |
| fixed_size<> | [length]            | Length string is specified length              |
| size_gt<>    | [length]            | Length string is greater than specified length |
| size_lt<>    | [length]            | Length string is less less specified length    |
| not_empty<>  | []                  | String parameter is not empty                  |
| one_of<>     | [[val1, val2, ...]] | String is one of the specified values          |

**Array validators**
| Function               | Arguments           | Description                                         |
| ---------------------- | ------------------- | --------------------------------------------------- |
| unique<>               | []                  | Contains no duplicates                              |
| subset_of<>            | [[val1, val2, ...]] | Every element is one of the list                    |
| fixed_size<>           | [length]            | Number of elements is specified length              |
| size_gt<>              | [length]            | Number of elements is greater than specified length |
| size_lt<>              | [length]            | Number of elements is less less specified length    |
| not_empty<>            | []                  | Has at-least one element                            |
| element_bounds<>       | [lower, upper]      | Bounds checking each element (inclusive)            |
| lower_element_bounds<> | [lower]             | Lower bound for each element (inclusive)            |
| upper_element_bounds<> | [upper]             | Upper bound for each element (inclusive)            |

Note: `element_bounds<>` cannot be mixed with `lower_element_bounds<>` or `upper_element_bounds<>`.

### Custom validator functions
Validators are functions that return a `tl::expected<void, std::string>` type and accept a `rclcpp::Parameter const&` as their first argument and any number of arguments after that can be specified in YAML.
Validators are C++ functions defined in a header file similar to the example shown below.

Here is an example custom validator.

```c++
#include <rclcpp/rclcpp.hpp>

#include <fmt/core.h>
#include <tl/expected.hpp>

namespace my_project {

tl::expected<void, std::string> integer_equal_value(
    rclcpp::Parameter const& parameter, int expected_value) {
  int param_value = parameter.as_int();
    if (param_value != expected_value) {
        return tl::make_unexpected(fmt::format(
            "Invalid value {} for parameter {}. Expected {}"
            param_value, parameter.get_name(), expected_value);

  return {};
}

}  // namespace my_project
```

Add it to `CMakeLists.txt`

```cmake
generate_parameter_library(
  turtlesim_parameters # cmake target name for the parameter library
  src/turtlesim_parameters.yaml # path to input yaml file
  src/example_validators.hpp # path to the custom validator
)
```

To configure a parameter to be validated with the custom validator function `integer_equal_value` with an `expected_value` of `3` you could would this to the YAML.
```yaml
validation:
  "my_project::integer_equal_value": [3]
```

### Nested structures
After the top-level key, every subsequent non-leaf key will generate a nested C++ struct. The struct instance will have
the same name as the key.

```yaml
cpp_name_space:
  nest1:
    nest2:
      param_name: # this is a leaf
        type: string_array
```

The generated parameter value can then be accessed with `params.nest1.nest2.param_name`

### Mapped parameters
You can use parameter maps, where a map with keys from another `string_array` parameter is created. Add the `__map_` prefix followed by the key parameter name as follows:

```yaml
cpp_name_space:
  joints:
    type: string_array
    default_value: ["joint1", "joint2", "joint3"]
    description: "specifies which joints will be used by the controller"
  interfaces:
    type: string_array
    default_value: ["position", "velocity", "acceleration"]
    description: "interfaces to be used by the controller"
  # nested mapped example
  gain:
    __map_joints: # create a map with joints as keys
      __map_interfaces:  # create a map with interfaces as keys
        value:
          type: double
  # simple mapped example
  pid:
    __map_joints: # create a map with joints as keys
      values:
        type: double_array
```

The generated parameter value for the nested map example can then be accessed with:

**C++**

```c++
params.gain.joints_map.at("joint1").interfaces_map.at("position").value
```

**Python**

```python
params.gain.get_entry("joint1").get_entry("position").value
```

#### Key array scope resolution

The `key` used by a `__map_<key>` segment does not need to be defined at the root namespace level. It can also be a **sibling** within the same struct, or defined anywhere in a parent scope.
This allows you to co-locate the key array alongside the map it controls:

```yaml
cpp_name_space:
  # key array defined as a sibling of the map that uses it
  nested_map:
    entries:
      type: string_array
      default_value: ["entry1", "entry2"]
      description: "Keys for the nested map"
    __map_entries: # resolved to nested_map.entries (sibling scope)
      value:
        type: double
        default_value: 1.0
        description: "A value keyed by entries"
```

> **Note:** Scope resolution searches the current struct first, then walks up to parent scopes. If the key array is not found in any scope, the bare name is used as a fallback.

### Use generated struct in Cpp
The generated header file is named based on the target library name you passed as the first argument to the cmake function.
If you specified it to be `turtlesim_parameters` you can then include the generated code with `#include <turtlesim/turtlesim_parameters.hpp>`.
```c++
#include <turtlesim/turtlesim_parameters.hpp>
```

Note that this header can also be used from another package:
```cmake
cmake_minimum_required(VERSION 3.8)
project(my_other_package)


include(GNUInstallDirs)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(turtelsim REQUIRED)

add_library(my_lib src/my_lib.cpp)
target_include_directories(my_lib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)
target_link_libraries(my_lib PUBLIC turtlesim::turtlesim_parameters)

#############
## Install ##
#############

install(DIRECTORY include/${PROJECT_NAME}/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME})

install(TARGETS my_lib
  EXPORT ${PROJECT_NAME}Targets
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION lib/${PROJECT_NAME})

ament_export_targets(${PROJECT_NAME}Targets HAS_LIBRARY_TARGET)
ament_export_dependencies(turtlesim)
ament_package()
```

In your initialization code, create a `ParamListener` which will declare and get the parameters.
An exception will be thrown if any validation fails or any required parameters were not set.
Then call `get_params` on the listener to get a copy of the `Params` struct.
```c++
auto param_listener = std::make_shared<turtlesim::ParamListener>(node);
auto params = param_listener->get_params();
```

### Dynamic Parameters
If you are using dynamic parameters, you can use the following code to check if any of your parameters have changed and then get a new copy of the `Params` struct.
```c++
if (param_listener->is_old(params_)) {
  params_ = param_listener->get_params();
}
```

Alternatively, you can bind a callback function that triggers whenever a parameter is updated. When activated, the callback receives the updated parameters as an argument.
```c++
parameter_listener.setUserCallback([this](const auto& params) { reconfigure_callback(params); });
```

### Parameter documentation

In some cases, parameters might be unknown only at compile-time, and cannot be part of the generated C++ code. However, for documentation purpose of such parameters, the type `none` was introduced.

Parameters with `none` type won't generate any C++ code, but can exist to describe the expected name or namespace, that might be declared by an external piece of code and used in an override.

A typical use case is a controller, loading pluginlib-based filters, that themselves require (and declare) parameters in a known structure.

Example of declarative YAML

```yaml
force_torque_broadcaster_controller:
  sensor_name:
    type: string
    default_value: ""
    description: "Name of the sensor used as prefix for interfaces if there are no individual interface names defined."
  frame_id:
    type: string
    default_value: ""
    description: "Sensor's frame_id in which values are published."
  sensor_filter_chain:
    type: none
    description: "Map of parameters that defines a filter chain, containing filterN as key and underlying map of parameters needed for a specific filter. See <some docs> for more details."
```

Example of parameters for that controller

```yaml
force_torque_broadcaster_controller:
  ros__parameters:
    sensor_name: "fts_sensor"
    frame_id: "fts_sensor_frame"
    sensor_filter_chain:
      filter1:
        type: "control_filters/LowPassFilterWrench"
        name: "low_pass_filter"
        params:
          sampling_frequency: 200.0
          damping_frequency: 50.0
          damping_intensity: 1.0
```


### Example Project
See [cpp example](https://github.com/PickNikRobotics/generate_parameter_library/tree/main/example) or [python example](https://github.com/PickNikRobotics/generate_parameter_library/tree/main/example_python) for complete examples of how to use the generate_parameter_library.

### Generated code output
The generated code primarily consists of two major components:
1) `struct Params` that contains values of all parameters and
2) `class ParamListener` that handles parameter declaration, updating, and validation.
   The general structure is shown below.

```cpp
namespace cpp_namespace {

struct Params {
  int param_name = 3;
  struct {
    struct{
      std::string param_name;
      // arbitrary nesting depth...
    } nest2;
  } nest1;
  // for detecting if the parameter struct has been updated
  rclcpp::Time __stamp;
};

class ParamListener {
 public:
  ParamListener(rclcpp::ParameterInterface);
  ParamListener(rclcpp::Node::SharedPtr node)
    : ParameterListener(node->get_parameters_interface()) {}
  ParamListener(rclcpp_lifecycle::LifecycleNode::SharedPtr node)
    : ParameterListener(node->get_parameters_interface()) {}

  // create a copy of current parameter values
  Params get_params() const;

  // returns true if parameters have been updated since last time get_params was called
  bool is_old(Params const& other) const;

  // loop over all parameters: perform validation then update
  rcl_interfaces::msg::SetParametersResult update(const std::vector<rclcpp::Parameter> &parameters);

  // declare all parameters and throw an exception if a non-optional value is missing or validation fails
  void declare_params(const std::shared_ptr<rclcpp::node_interfaces::NodeParametersInterface>& parameters_interface);

 private:
  Params params_;
};

} // namespace cpp_namespace
```
The structure of the `Params` struct and the logic for declaring and updating parameters is generated from a YAML file specification.

### Generate markdown documentation

Using generate_parameter_library you can generate a Markdown-file for your `parameters.yaml` file.
```
generate_parameter_library_markdown --input_yaml example/src/parameters.yaml --output_markdown_file parameters.md
```

This will generate a file `parameters.md` in the current folder that contains a markdown
representation of the `parameters.yaml` file that you can directly include into your documentation.

# FAQ

Q. What happens if I declare a parameter twice? Will I get an error at runtime?

A. The declare routine that is generated checks to see if each parameter has been declared first before declaring it. Because of this you can declare a parameter twice but it will only have the properties of the first time you declared it. Here is some example generated code.
```cpp
if (!parameters_interface_->has_parameter(prefix_ + "scientific_notation_num")) {
    rcl_interfaces::msg::ParameterDescriptor descriptor;
    descriptor.description = "Test scientific notation";
    descriptor.read_only = false;
    auto parameter = to_parameter_value(updated_params.scientific_notation_num);
    parameters_interface_->declare_parameter(prefix_ + "scientific_notation_num", parameter, descriptor);
}
```

Q: How do I log when parameters change?

A. The generated library outputs debug logs whenever a parameter is read from ROS.


## Build status

ROS2 Distro | Branch | Build status | Documentation | Package Build
:---------: | :----: | :----------: | :-----------: | :---------------:
**Rolling** | [`main`](https://github.com/PickNikRobotics/generate_parameter_library/tree/main) | [![Rolling Binary Build](https://github.com/PickNikRobotics/generate_parameter_library/actions/workflows/rolling-binary-build.yaml/badge.svg?branch=main)](https://github.com/PickNikRobotics/generate_parameter_library/actions/workflows/rolling-binary-build.yaml?branch=main) <br> [![Rolling Semi-Binary Build](https://github.com/PickNikRobotics/generate_parameter_library/actions/workflows/rolling-semi-binary-build.yaml/badge.svg?branch=main)](https://github.com/PickNikRobotics/generate_parameter_library/actions/workflows/rolling-semi-binary-build.yaml?branch=main) <br> [![build.ros2.org](https://build.ros2.org/buildStatus/icon?job=Rdev__generate_parameter_library__ubuntu_resolute_amd64&subject=build.ros2.org)](https://build.ros2.org/job/Rdev__generate_parameter_library__ubuntu_resolute_amd64/) | [Documentation](https://docs.ros.org/en/rolling/p/generate_parameter_library/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Rbin_uR64__generate_parameter_library__ubuntu_resolute_amd64__binary)](https://build.ros2.org/job/Rbin_uR64__generate_parameter_library__ubuntu_resolute_amd64__binary/) <br> [![Build Status](https://build.ros2.org/buildStatus/icon?job=Rbin_uR64__generate_parameter_library_py__ubuntu_resolute_amd64__binary)](https://build.ros2.org/job/Rbin_uR64__generate_parameter_library_py__ubuntu_resolute_amd64__binary/)
**Lyrical** | [`main`](https://github.com/PickNikRobotics/generate_parameter_library/tree/main) | see above <br> [![build.ros2.org](https://build.ros2.org/buildStatus/icon?job=Ldev__generate_parameter_library__ubuntu_resolute_amd64&subject=build.ros2.org)](https://build.ros2.org/job/Ldev__generate_parameter_library__ubuntu_resolute_amd64/) | [Documentation](https://docs.ros.org/en/rolling/p/generate_parameter_library/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Lbin_uR64__generate_parameter_library__ubuntu_resolute_amd64__binary)](https://build.ros2.org/job/Lbin_uR64__generate_parameter_library__ubuntu_resolute_amd64__binary/) <br> [![Build Status](https://build.ros2.org/buildStatus/icon?job=Lbin_uR64__generate_parameter_library_py__ubuntu_resolute_amd64__binary)](https://build.ros2.org/job/Lbin_uR64__generate_parameter_library_py__ubuntu_resolute_amd64__binary/)
**Kilted** | [`humble`](https://github.com/PickNikRobotics/generate_parameter_library/tree/humble) | see below <br> [![build.ros2.org](https://build.ros2.org/buildStatus/icon?job=Kdev__generate_parameter_library__ubuntu_noble_amd64&subject=build.ros2.org)](https://build.ros2.org/job/Kdev__generate_parameter_library__ubuntu_noble_amd64/) | [Documentation](https://docs.ros.org/en/kilted/p/generate_parameter_library/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Kbin_uN64__generate_parameter_library__ubuntu_noble_amd64__binary)](https://build.ros2.org/job/Kbin_uN64__generate_parameter_library__ubuntu_noble_amd64__binary/) <br> [![Build Status](https://build.ros2.org/buildStatus/icon?job=Kbin_uN64__generate_parameter_library_py__ubuntu_noble_amd64__binary)](https://build.ros2.org/job/Kbin_uN64__generate_parameter_library_py__ubuntu_noble_amd64__binary/)
**Jazzy** | [`humble`](https://github.com/PickNikRobotics/generate_parameter_library/tree/humble) | see below <br> [![build.ros2.org](https://build.ros2.org/buildStatus/icon?job=Jdev__generate_parameter_library__ubuntu_noble_amd64&subject=build.ros2.org)](https://build.ros2.org/job/Jdev__generate_parameter_library__ubuntu_noble_amd64/) | [Documentation](https://docs.ros.org/en/jazzy/p/generate_parameter_library/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Jbin_uN64__generate_parameter_library__ubuntu_noble_amd64__binary)](https://build.ros2.org/job/Jbin_uN64__generate_parameter_library__ubuntu_noble_amd64__binary/) <br> [![Build Status](https://build.ros2.org/buildStatus/icon?job=Jbin_uN64__generate_parameter_library_py__ubuntu_noble_amd64__binary)](https://build.ros2.org/job/Jbin_uN64__generate_parameter_library_py__ubuntu_noble_amd64__binary/)
**Humble** | [`humble`](https://github.com/PickNikRobotics/generate_parameter_library/tree/humble) | [![Humble Binary Build](https://github.com/PickNikRobotics/generate_parameter_library/actions/workflows/humble-binary-build.yaml/badge.svg?branch=humble)](https://github.com/PickNikRobotics/generate_parameter_library/actions/workflows/humble-binary-build.yaml?branch=humble) <br> [![Humble Semi-Binary Build](https://github.com/PickNikRobotics/generate_parameter_library/actions/workflows/humble-semi-binary-build.yaml/badge.svg?branch=humble)](https://github.com/PickNikRobotics/generate_parameter_library/actions/workflows/humble-semi-binary-build.yaml?branch=humble) <br> [![build.ros2.org](https://build.ros2.org/buildStatus/icon?job=Hdev__generate_parameter_library__ubuntu_jammy_amd64&subject=build.ros2.org)](https://build.ros2.org/job/Hdev__generate_parameter_library__ubuntu_jammy_amd64/) | [Documentation](https://docs.ros.org/en/humble/p/generate_parameter_library/) | [![Build Status](https://build.ros2.org/buildStatus/icon?job=Hbin_uJ64__generate_parameter_library__ubuntu_jammy_amd64__binary)](https://build.ros2.org/job/Hbin_uJ64__generate_parameter_library__ubuntu_jammy_amd64__binary/) <br> [![Build Status](https://build.ros2.org/buildStatus/icon?job=Hbin_uJ64__generate_parameter_library_py__ubuntu_jammy_amd64__binary)](https://build.ros2.org/job/Hbin_uJ64__generate_parameter_library_py__ubuntu_jammy_amd64__binary/)
