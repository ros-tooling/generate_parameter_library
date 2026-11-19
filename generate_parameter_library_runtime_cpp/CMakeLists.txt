cmake_minimum_required(VERSION 3.20)
project(generate_parameter_library_runtime_cpp NONE)

find_package(ament_cmake REQUIRED)

# Nothing to build: package.xml carries the runtime dependencies of generated code.
ament_package()
