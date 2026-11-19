cmake_minimum_required(VERSION 3.16)
project(generate_parameter_library_example_external)

if(CMAKE_CXX_COMPILER_ID MATCHES "(GNU|Clang)")
    add_compile_options(-Wall -Wextra -Wpedantic -Wshadow -Wconversion -Wsign-conversion -Wold-style-cast)
endif()

find_package(ros2_control_cmake REQUIRED)
export_windows_symbols()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(generate_parameter_library_example REQUIRED)

add_library(minimal_publisher_external SHARED
  src/minimal_publisher_external.cpp
)
target_include_directories(minimal_publisher_external PUBLIC
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/generate_parameter_library_example_external>
)
target_link_libraries(minimal_publisher_external
  PUBLIC
    rclcpp::rclcpp
    rclcpp_components::component
    generate_parameter_library_example::admittance_controller_parameters
)
rclcpp_components_register_node(minimal_publisher_external
  PLUGIN "admittance_controller::MinimalPublisher"
  EXECUTABLE test_node
)

install(
  DIRECTORY include/
  DESTINATION include/generate_parameter_library_example_external
)

install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}/
)

install(TARGETS minimal_publisher_external
  EXPORT export_generate_parameter_library_example_external
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(
  TARGETS test_node
  DESTINATION lib/generate_parameter_library_example_external
)

if(BUILD_TESTING)
  find_package(launch_testing_ament_cmake REQUIRED)
  add_launch_test(test/launch.test.py
    TIMEOUT 50
  )
endif()

ament_export_targets(export_generate_parameter_library_example_external HAS_LIBRARY_TARGET)
ament_export_dependencies(rclcpp rclcpp_components generate_parameter_library_example)

ament_package()
