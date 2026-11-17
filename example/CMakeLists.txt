cmake_minimum_required(VERSION 3.16)
project(generate_parameter_library_example)

if(CMAKE_CXX_COMPILER_ID MATCHES "(GNU|Clang)")
    add_compile_options(-Wall -Wextra -Wpedantic -Wshadow -Wconversion -Wsign-conversion -Wold-style-cast)
endif()

find_package(ros2_control_cmake REQUIRED)
export_windows_symbols()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(generate_parameter_library REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(rclpy REQUIRED)

generate_parameter_library(admittance_controller_parameters
  src/parameters.yaml
  include/generate_parameter_library_example/example_validators.hpp
)

add_library(minimal_publisher SHARED
  src/minimal_publisher.cpp
)
target_include_directories(minimal_publisher PUBLIC
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/generate_parameter_library_example>
)
target_link_libraries(minimal_publisher
  PUBLIC
    admittance_controller_parameters
    rclcpp::rclcpp
    rclcpp_components::component
)
rclcpp_components_register_node(minimal_publisher
  PLUGIN "admittance_controller::MinimalPublisher"
  EXECUTABLE test_node
)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  # example_test_gtest
  add_rostest_with_parameters_gtest(test_example_gtest test/example_test_gtest.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test/example_params.yaml)
  target_include_directories(test_example_gtest PRIVATE include)
  target_link_libraries(test_example_gtest admittance_controller_parameters rclcpp::rclcpp)
  # descriptor_test_gtest
  add_rostest_with_parameters_gtest(test_descriptor_gtest test/descriptor_test_gtest.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test/example_params.yaml)
  target_include_directories(test_descriptor_gtest PRIVATE include)
  target_link_libraries(test_descriptor_gtest admittance_controller_parameters rclcpp::rclcpp)

  find_package(ament_cmake_gmock REQUIRED)
  add_rostest_with_parameters_gmock(test_example_gmock test/example_test_gmock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/test/example_params.yaml)
  target_include_directories(test_example_gmock PRIVATE include)
  target_link_libraries(test_example_gmock admittance_controller_parameters rclcpp::rclcpp)

  # test_params_consistency - GMock test verifying consistency between get_params() and ROS2 parameter server
  ament_add_gmock(test_params_consistency test/test_params_consistency.cpp)
  target_include_directories(test_params_consistency PRIVATE include)
  target_link_libraries(test_params_consistency admittance_controller_parameters rclcpp::rclcpp)

  find_package(launch_testing_ament_cmake REQUIRED)
  add_launch_test(test/launch.test.py
    TIMEOUT 50
  )

  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_installed_definition test/test_installed_definition.py)
endif()

install(
  DIRECTORY include/
  DESTINATION include/generate_parameter_library_example
)

install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}/
)

install(TARGETS minimal_publisher admittance_controller_parameters
  EXPORT export_generate_parameter_library_example
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(
  TARGETS test_node
  DESTINATION lib/generate_parameter_library_example
)

ament_export_targets(export_generate_parameter_library_example HAS_LIBRARY_TARGET)
ament_export_dependencies(rclcpp rclcpp_components)
ament_package()
