# Copyright 2022 PickNik Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the PickNik Inc. nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


macro(generate_parameter_library LIB_NAME YAML_FILE)
  unset(generate_parameter_library_cpp_BIN CACHE)  # Unset the cache variable
  find_program(generate_parameter_library_cpp_BIN NAMES "generate_parameter_library_cpp")
  if(NOT generate_parameter_library_cpp_BIN)
    message(FATAL_ERROR "generate_parameter_library_cpp() variable 'generate_parameter_library_cpp_BIN' must not be empty")
  endif()

  # Make the include directory
  set(LIB_INCLUDE_DIR ${CMAKE_CURRENT_BINARY_DIR}/include/${PROJECT_NAME})
  file(MAKE_DIRECTORY ${LIB_INCLUDE_DIR})

  # Optional 3rd parameter for the user defined validation header
  if(${ARGC} EQUAL 3)
    cmake_path(SET IN_VALIDATE_HEADER ${CMAKE_CURRENT_SOURCE_DIR})
    cmake_path(APPEND IN_VALIDATE_HEADER ${ARGV2})

    cmake_path(GET IN_VALIDATE_HEADER FILENAME VALIDATE_HEADER_FILENAME)
    cmake_path(SET VALIDATE_HEADER ${LIB_INCLUDE_DIR})
    cmake_path(APPEND VALIDATE_HEADER ${VALIDATE_HEADER_FILENAME})

    # Copy the header file into the include directory
    file(COPY ${IN_VALIDATE_HEADER} DESTINATION ${LIB_INCLUDE_DIR})
  endif()

  # Set the yaml file parameter to be relative to the current source dir
  set(YAML_FILE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/${YAML_FILE})

  # Set the output parameter header file name
  set(PARAM_HEADER_FILE ${LIB_INCLUDE_DIR}/${LIB_NAME}.hpp)

  # Generate the header for the library
  add_custom_command(
    OUTPUT ${PARAM_HEADER_FILE}
    COMMAND ${generate_parameter_library_cpp_BIN} ${PARAM_HEADER_FILE} ${YAML_FILE_PATH} ${VALIDATE_HEADER_FILENAME}
    DEPENDS ${YAML_FILE_PATH} ${VALIDATE_HEADER}
    COMMENT
    "Running `${generate_parameter_library_cpp_BIN} ${PARAM_HEADER_FILE} ${YAML_FILE_PATH} ${VALIDATE_HEADER_FILENAME}`"
    VERBATIM
  )

  # Create the library target
  add_library(${LIB_NAME} INTERFACE ${PARAM_HEADER_FILE} ${VALIDATE_HEADER})
  target_include_directories(${LIB_NAME} INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
    $<INSTALL_INTERFACE:include>
  )
  set_target_properties(${LIB_NAME} PROPERTIES LINKER_LANGUAGE CXX)
  target_link_libraries(${LIB_NAME} INTERFACE
    fmt::fmt
    rclcpp::rclcpp
    rclcpp_lifecycle::rclcpp_lifecycle
    rsl::rsl
    tcb_span::tcb_span
    tl::expected
  )
  install(DIRECTORY ${LIB_INCLUDE_DIR} DESTINATION include)
  ament_export_dependencies(
    fmt rclcpp rclcpp_lifecycle rsl tcb_span
    tl-expected
  )
endmacro()


function(generate_parameter_module LIB_NAME YAML_FILE)
  find_program(generate_parameter_library_python_BIN NAMES "generate_parameter_library_python")
  if(NOT generate_parameter_library_python_BIN)
    message(FATAL_ERROR "generate_parameter_library_python() variable 'generate_parameter_library_python_BIN' must not be empty")
  endif()

  # Optional 3rd parameter for the user defined validation header
  if(${ARGC} EQUAL 3)
    set(VALIDATE_HEADER_FILENAME ${ARGV2})
  endif()

  # Set the yaml file parameter to be relative to the current source dir
  set(YAML_FILE ${CMAKE_CURRENT_SOURCE_DIR}/${YAML_FILE})

  # Create a build-local output directory for the generated Python module
  set(PY_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/generate_parameter_module_temp)
  file(MAKE_DIRECTORY ${PY_BUILD_DIR})

  find_package(ament_cmake_python)
  ament_get_python_install_dir(python_install_dir)

  # Generate into the build tree, not into CMAKE_INSTALL_PREFIX
  set(PARAM_HEADER_FILE ${PY_BUILD_DIR}/${LIB_NAME}.py)

  # Generate the module for Python
  add_custom_command(
          OUTPUT ${PARAM_HEADER_FILE}
          COMMAND ${generate_parameter_library_python_BIN} ${PARAM_HEADER_FILE} ${YAML_FILE} ${VALIDATE_HEADER_FILENAME}
          DEPENDS ${YAML_FILE}
          COMMENT
          "Running `${generate_parameter_library_python_BIN} ${PARAM_HEADER_FILE} ${YAML_FILE} ${VALIDATE_HEADER_FILENAME}`"
          VERBATIM
  )

  # Create the library target
  add_library(${LIB_NAME} INTERFACE ${PARAM_HEADER_FILE})

  # Install the generated module into the Python site-packages dir
  install(FILES ${PARAM_HEADER_FILE} DESTINATION ${CMAKE_INSTALL_PREFIX}/${python_install_dir}/${PROJECT_NAME})
endfunction()

# create custom test function to pass yaml file into test main
function(add_rostest_with_parameters_gtest TARGET SOURCES YAML_FILE)
  add_executable(${TARGET} ${SOURCES})
  _ament_cmake_gtest_find_gtest()
  target_include_directories(${TARGET} PUBLIC "${GTEST_INCLUDE_DIRS}")
  target_link_libraries(${TARGET} ${GTEST_LIBRARIES})
  set(executable "$<TARGET_FILE:${TARGET}>")
  set(result_file "${AMENT_TEST_RESULTS_DIR}/${PROJECT_NAME}/${TARGET}.gtest.xml")
  ament_add_test(
    ${TARGET}
    COMMAND ${executable} --ros-args --params-file ${YAML_FILE} --
    --gtest_output=xml:${result_file}
    OUTPUT_FILE ${AMENT_TEST_RESULTS_DIR}/${PROJECT_NAME}/${TARGET}.txt
    RESULT_FILE ${result_file}
  )
endfunction()

function(add_rostest_with_parameters_gmock TARGET SOURCES YAML_FILE)
  add_executable(${TARGET} ${SOURCES})
  _ament_cmake_gmock_find_gmock()
  target_include_directories(${TARGET} PUBLIC "${GMOCK_INCLUDE_DIRS}")
  target_link_libraries(${TARGET} ${GMOCK_LIBRARIES})
  set(executable "$<TARGET_FILE:${TARGET}>")
  set(result_file "${AMENT_TEST_RESULTS_DIR}/${PROJECT_NAME}/${TARGET}.gtest.xml")
  ament_add_test(
    ${TARGET}
    COMMAND ${executable} --ros-args --params-file ${YAML_FILE} --
    --gtest_output=xml:${result_file}
    OUTPUT_FILE ${AMENT_TEST_RESULTS_DIR}/${PROJECT_NAME}/${TARGET}.txt
    RESULT_FILE ${result_file}
  )
endfunction()
