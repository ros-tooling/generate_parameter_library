^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package generate_parameter_module_example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.4.0 (2026-11-17)
------------------
* Install parameter definitions to share/<package>/parameter_definitions (`#419 <https://github.com/ros-tooling/generate_parameter_library/issues/419>`_)
* Name the offending element and bound in element bound messages (`#410 <https://github.com/ros-tooling/generate_parameter_library/issues/410>`_)
* Use implentation.yaml for example_python tests (`#399 <https://github.com/ros-tooling/generate_parameter_library/issues/399>`_)
* Fix python install paths (`#393 <https://github.com/ros-tooling/generate_parameter_library/issues/393>`_)
* Contributors: Christoph Fröhlich, Marq Rasmussen

1.3.1 (2026-10-05)
------------------
* fix that if no parameter is updated, the user callback is not called (`#383 <https://github.com/ros-tooling/generate_parameter_library/issues/383>`_)
* Contributors: Fabian Hirmann

1.3.0 (2026-07-24)
------------------
* Accept quotes in description and additional constraints (`#357 <https://github.com/ros-tooling/generate_parameter_library/issues/357>`_)
* Use a shared symlinked parameter file in all examples (`#361 <https://github.com/ros-tooling/generate_parameter_library/issues/361>`_)
* Fix floating_point_range numerical values (`#360 <https://github.com/ros-tooling/generate_parameter_library/issues/360>`_)
* Contributors: Christoph Fröhlich, Hugal31

1.2.0 (2026-06-09)
------------------
* add gitignore for generated files in example_python (`#356 <https://github.com/ros-tooling/generate_parameter_library/issues/356>`_)
* Made fields in python structs assigned per-instance instead of at the class scope (`#351 <https://github.com/ros-tooling/generate_parameter_library/issues/351>`_)
* Fix ParameterDescription of exclusive bounds (`#339 <https://github.com/ros-tooling/generate_parameter_library/issues/339>`_)
* Contributors: Alex Navarro, Christoph Fröhlich, Jonas Otto

1.1.0 (2026-05-14)
------------------

1.0.1 (2026-05-06)
------------------

1.0.0 (2026-04-22)
------------------
* Implement string_array_fixed_XX (`#341 <https://github.com/ros-tooling/generate_parameter_library/issues/341>`_)
* Fix conflicting validators (`#336 <https://github.com/ros-tooling/generate_parameter_library/issues/336>`_)
* Fix rst syntax parsing in parameter description (`#338 <https://github.com/ros-tooling/generate_parameter_library/issues/338>`_)
* Contributors: Christoph Fröhlich, Mat198

0.8.0 (2026-03-22)
------------------
* Testing consistency of parameters update (Python) (`#327 <https://github.com/ros-tooling/generate_parameter_library/issues/327>`_)
* Fix nested mapped parameters map (`#306 <https://github.com/ros-tooling/generate_parameter_library/issues/306>`_)
* Contributors: Mat198, Nick Laurenson

0.7.0 (2026-02-22)
------------------
* Move linters to pre-commit (`#298 <https://github.com/ros-tooling/generate_parameter_library/issues/298>`_)
* Contributors: Christoph Fröhlich

0.6.0 (2025-12-06)
------------------
* Update pre-commit hooks (`#288 <https://github.com/ros-tooling/generate_parameter_library/issues/288>`_)
* fix setuptools deprecation (`#272 <https://github.com/ros-tooling/generate_parameter_library/issues/272>`_)
* Update maintainers for GBP release team (`#282 <https://github.com/ros-tooling/generate_parameter_library/issues/282>`_)
* Contributors: Christoph Fröhlich, Nathan Brooks, mosfet80

0.5.0 (2025-06-12)
------------------
* Add some new maintainers for ROS releases (`#263 <https://github.com/ros-tooling/generate_parameter_library/issues/263>`_)
* Contributors: Nathan Brooks

0.4.0 (2025-01-13)
------------------
* Unit test friendly folder structure for Python examples (`#237 <https://github.com/ros-tooling/generate_parameter_library/issues/237>`_)
* Fix flake8 error in publisher example (`#229 <https://github.com/ros-tooling/generate_parameter_library/issues/229>`_)
* Contributors: Sebastian Castro

0.3.9 (2024-10-27)
------------------
* Add "additional_constraints" support (`#221 <https://github.com/ros-tooling/generate_parameter_library/issues/221>`_)
* Drop yaml brackets for consistency and readability (`#203 <https://github.com/ros-tooling/generate_parameter_library/issues/203>`_)
* Contributors: David Revay, Tim Clephas

0.3.8 (2024-03-27)
------------------
* Restore functionality for mapped params with no struct name (`#185 <https://github.com/ros-tooling/generate_parameter_library/issues/185>_`)
* Fix newline issue (`#176 <https://github.com/ros-tooling/generate_parameter_library/issues/176>`_)
  * fix new line rendering for Python
* Support nested mapped parameters (`#166 <https://github.com/ros-tooling/generate_parameter_library/issues/166>`_)
* Contributors: Paul Gesel, Sebastian Castro

0.3.7 (2024-01-12)
------------------
* Fix rolling CI (`#162 <https://github.com/ros-tooling/generate_parameter_library/issues/162>`_)
* Split example/README.md into C++ and Python version; updated content (`#138 <https://github.com/ros-tooling/generate_parameter_library/issues/138>`_)
* Contributors: Paul Gesel, chriseichmann

0.3.6 (2023-07-31)
------------------
* Prevent module import  when running `setup.py clean` (`#137 <https://github.com/ros-tooling/generate_parameter_library/issues/137>`_)
* Contributors: Paul Gesel

0.3.5 (2023-07-28)
------------------
* add dependency to python example package (`#136 <https://github.com/ros-tooling/generate_parameter_library/issues/136>`_)
* Contributors: Paul Gesel

0.3.4 (2023-07-24)
------------------
* Fix Python install (`#122 <https://github.com/ros-tooling/generate_parameter_library/issues/122>`_)
* Add Python support for generate_parameter_library (`#110 <https://github.com/ros-tooling/generate_parameter_library/issues/110>`_)
  Co-authored-by: Tyler Weaver <tyler@picknik.ai>
* Contributors: Paul Gesel
