^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package generate_parameter_library_py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.4.0 (2026-11-17)
------------------
* Escape text in generated C++ and Python code (`#405 <https://github.com/ros-tooling/generate_parameter_library/issues/405>`_)
* Install parameter definitions to share/<package>/parameter_definitions (`#419 <https://github.com/ros-tooling/generate_parameter_library/issues/419>`_)
* Report wrong default_value types as definition errors (`#408 <https://github.com/ros-tooling/generate_parameter_library/issues/408>`_)
* Validator: name nested sequences in array type errors (`#418 <https://github.com/ros-tooling/generate_parameter_library/issues/418>`_)
* Validator: add --node to check only the node that loads the configs (`#416 <https://github.com/ros-tooling/generate_parameter_library/issues/416>`_)
* Validator: merge several --config files like the parameter files of one node (`#413 <https://github.com/ros-tooling/generate_parameter_library/issues/413>`_)
* Recognize a parameter by its type field, not by its first key (`#407 <https://github.com/ros-tooling/generate_parameter_library/issues/407>`_)
* Remove dead code (`#412 <https://github.com/ros-tooling/generate_parameter_library/issues/412>`_)
* Accept an output file name without a directory in the generators (`#409 <https://github.com/ros-tooling/generate_parameter_library/issues/409>`_)
* Load parameter definitions with the safe YAML loader (`#406 <https://github.com/ros-tooling/generate_parameter_library/issues/406>`_)
* Name the offending element and bound in element bound messages (`#410 <https://github.com/ros-tooling/generate_parameter_library/issues/410>`_)
* Python install paths: clean up generated modules and extend CI coverage (`#400 <https://github.com/ros-tooling/generate_parameter_library/issues/400>`_)
* Add a standalone configuration validator (`#312 <https://github.com/ros-tooling/generate_parameter_library/issues/312>`_) (`#388 <https://github.com/ros-tooling/generate_parameter_library/issues/388>`_)
* Fix python install paths (`#393 <https://github.com/ros-tooling/generate_parameter_library/issues/393>`_)
* Validate bound validators against parameter types (`#373 <https://github.com/ros-tooling/generate_parameter_library/issues/373>`_)
* Validate fixed-size parameter defaults (`#374 <https://github.com/ros-tooling/generate_parameter_library/issues/374>`_)
* Contributors: Christoph Fröhlich, Daniiiil1, Davide Faconti, Marq Rasmussen

1.3.1 (2026-10-05)
------------------
* fix that if no parameter is updated, the user callback is not called (`#383 <https://github.com/PickNikRobotics/generate_parameter_library/issues/383>`_)
* Contributors: Fabian Hirmann

1.3.0 (2026-07-24)
------------------
* Accept quotes in description and additional constraints (`#357 <https://github.com/PickNikRobotics/generate_parameter_library/issues/357>`_)
* Contributors: Hugal31

1.2.0 (2026-06-09)
------------------
* Made fields in python structs assigned per-instance instead of at the class scope (`#351 <https://github.com/PickNikRobotics/generate_parameter_library/issues/351>`_)
* Fix ParameterDescription of exclusive bounds (`#339 <https://github.com/PickNikRobotics/generate_parameter_library/issues/339>`_)
* Contributors: Alex Navarro, Christoph Fröhlich

1.1.0 (2026-05-14)
------------------

1.0.1 (2026-05-06)
------------------

1.0.0 (2026-04-22)
------------------
* Fix markdown generation for bounds/element-bounds (`#337 <https://github.com/PickNikRobotics/generate_parameter_library/issues/337>`_)
* Generate markdown documentation also for none type (`#345 <https://github.com/PickNikRobotics/generate_parameter_library/issues/345>`_)
* Implement string_array_fixed_XX (`#341 <https://github.com/PickNikRobotics/generate_parameter_library/issues/341>`_)
* Fix conflicting validators (`#336 <https://github.com/PickNikRobotics/generate_parameter_library/issues/336>`_)
* Fix rst syntax parsing in parameter description (`#338 <https://github.com/PickNikRobotics/generate_parameter_library/issues/338>`_)
* Remove deprecated parameter_traits (`#294 <https://github.com/PickNikRobotics/generate_parameter_library/issues/294>`_) (`#330 <https://github.com/PickNikRobotics/generate_parameter_library/issues/330>`_)
* Contributors: Christoph Fröhlich, Mat198

0.8.0 (2026-03-22)
------------------
* Fix nested mappings double dot bug (`#329 <https://github.com/PickNikRobotics/generate_parameter_library/issues/329>`_)
  Co-authored-by: Nathan <50861188+natrad100@users.noreply.github.com>
* Fix nested mapped parameters map (`#306 <https://github.com/PickNikRobotics/generate_parameter_library/issues/306>`_)
* Remove unused variables in pytest (`#317 <https://github.com/PickNikRobotics/generate_parameter_library/issues/317>`_)
* Contributors: Christoph Fröhlich, Nick Laurenson

0.7.0 (2026-02-22)
------------------
* Deprecate parameter_traits package and header file (`#297 <https://github.com/PickNikRobotics/generate_parameter_library/issues/297>`_)
* Move linters to pre-commit (`#298 <https://github.com/PickNikRobotics/generate_parameter_library/issues/298>`_)
* Contributors: Christoph Fröhlich

0.6.0 (2025-12-06)
------------------
* Use templated NodeT in c++ constructor  (`#274 <https://github.com/PickNikRobotics/generate_parameter_library/issues/274>`_)
* Update pre-commit hooks (`#288 <https://github.com/PickNikRobotics/generate_parameter_library/issues/288>`_)
* Improve logging message when a parameter is not set (`#279 <https://github.com/PickNikRobotics/generate_parameter_library/issues/279>`_)
* Account for nested map params (`#277 <https://github.com/PickNikRobotics/generate_parameter_library/issues/277>`_) (`#280 <https://github.com/PickNikRobotics/generate_parameter_library/issues/280>`_)
* Update maintainers for GBP release team (`#282 <https://github.com/PickNikRobotics/generate_parameter_library/issues/282>`_)
* fix setuptools deprecations (`#268 <https://github.com/PickNikRobotics/generate_parameter_library/issues/268>`_)
* Contributors: Ander González Tomé, Christoph Fröhlich, Gaël Écorchard, Nathan Brooks, Russ, mosfet80

0.5.0 (2025-06-12)
------------------
* Add `try_update_params` method (`#260 <https://github.com/PickNikRobotics/generate_parameter_library/issues/260>`_)
* Fix ros2_controllers issue`#1740 <https://github.com/PickNikRobotics/generate_parameter_library/issues/1740>`_ -Wreorder fix (`#264 <https://github.com/PickNikRobotics/generate_parameter_library/issues/264>`_)
* No need to default-construct logger in the declaration (`#252 <https://github.com/PickNikRobotics/generate_parameter_library/issues/252>`_)
* Add user callback python (`#254 <https://github.com/PickNikRobotics/generate_parameter_library/issues/254>`_)
* Add user callback (`#250 <https://github.com/PickNikRobotics/generate_parameter_library/issues/250>`_)
* Fix merge install for python packages (`#241 <https://github.com/PickNikRobotics/generate_parameter_library/issues/241>`_)
* Contributors: Darren Tsai, Dimitri Decious, Nathan Brooks, Sai Kishor Kothakota, Tim Clephas, Yannick de Hoop

0.4.0 (2025-01-13)
------------------
* Unit test friendly folder structure for Python examples (`#237 <https://github.com/PickNikRobotics/generate_parameter_library/issues/237>`_)
* Fix conversion typos (`#238 <https://github.com/PickNikRobotics/generate_parameter_library/issues/238>`_)
* Apply clang-tidy suggestions to `std::move` certain variables (`#228 <https://github.com/PickNikRobotics/generate_parameter_library/issues/228>`_)
* Contributors: Sebastian Castro

0.3.9 (2024-10-27)
------------------
* fix error with not being able to find unpack_parameter_dict when using set_params_from_dict (`#220 <https://github.com/PickNikRobotics/generate_parameter_library/issues/220>`_)
* Add "additional_constraints" support (`#221 <https://github.com/PickNikRobotics/generate_parameter_library/issues/221>`_)
* Use int64_t instead of int for parameter integer range, fixes `#199 <https://github.com/PickNikRobotics/generate_parameter_library/issues/199>`_ (`#214 <https://github.com/PickNikRobotics/generate_parameter_library/issues/214>`_)
* Fix floating point range for upper/lt/lt_eq validations (`#216 <https://github.com/PickNikRobotics/generate_parameter_library/issues/216>`_)
* Fix nested parameter in Python template (`#210 <https://github.com/PickNikRobotics/generate_parameter_library/issues/210>`_)
* Fix test on rolling CI (`#187 <https://github.com/PickNikRobotics/generate_parameter_library/issues/187>`_)
* Add ability for param_listener to load values from yaml dictionary (`#211 <https://github.com/PickNikRobotics/generate_parameter_library/issues/211>`_)
* Use exist_ok=True in makedirs instead of checking for existence first, in case of multiple concurrent processes (`#212 <https://github.com/PickNikRobotics/generate_parameter_library/issues/212>`_)
* Add Non-Blocking try_get_params Function for Real-Time Control Systems (`#205 <https://github.com/PickNikRobotics/generate_parameter_library/issues/205>`_)
* Drop yaml brackets for consistency and readability (`#203 <https://github.com/PickNikRobotics/generate_parameter_library/issues/203>`_)
* Contributors: Karan Khanna, Auguste Bourgois, David Revay, Emerson Knapp, Jacob Seibert, KentaKato, Marq Rasmussen, Paul Gesel, Tim Clephas

0.3.8 (2024-03-27)
------------------
* Restore functionality for mapped params with no struct name (`#185 <https://github.com/PickNikRobotics/generate_parameter_library/issues/185>_`)
* add # flake8: noqa to template (`#177 <https://github.com/PickNikRobotics/generate_parameter_library/issues/177>`_)
* Fix newline issue (`#176 <https://github.com/PickNikRobotics/generate_parameter_library/issues/176>`_)
  * fix new line rendering for Python
* Support nested mapped parameters (`#166 <https://github.com/PickNikRobotics/generate_parameter_library/issues/166>`_)
* Contributors: Paul Gesel, Sebastian Castro

0.3.7 (2024-01-12)
------------------
* fix Python runtime parameters bug (`#165 <https://github.com/PickNikRobotics/generate_parameter_library/issues/165>`_)
* markdown/rst: Support __map\_ and nested parameters (`#164 <https://github.com/PickNikRobotics/generate_parameter_library/issues/164>`_)
  * Support nested parameters and maps for RST
  * Add read_only info to RST template
  * Use map parameters for AutoDocumentation
  * Add test for markdown generation
  * Use jinja indentation instead of regex
  * Add dynamic_parameters also to DefaultConfig
  * Proper fromat of default yaml config
  * Proper format of the default yaml file
  * Fix imported function names
  * Add a jinja2 filter to create valid multiline c++ string literals
  * Handle empty strings for descriptions
* parse_yaml.py: keep the trailing newline (`#159 <https://github.com/PickNikRobotics/generate_parameter_library/issues/159>`_)
* Fix rolling CI (`#162 <https://github.com/PickNikRobotics/generate_parameter_library/issues/162>`_)
* parse_yaml.py: fix issue with typeguard (`#154 <https://github.com/PickNikRobotics/generate_parameter_library/issues/154>`_)
* Bugfixes on Python code generation (`#152 <https://github.com/PickNikRobotics/generate_parameter_library/issues/152>`_)
  * Fix raising of validation error
  * Fix inverse logic of 'unique' validator
* Fix sentence for size_lt (`#150 <https://github.com/PickNikRobotics/generate_parameter_library/issues/150>`_)
* Fix typeguard error (`#149 <https://github.com/PickNikRobotics/generate_parameter_library/issues/149>`_)
  For typeguard==3.0.2, `default_value: any` raised a `TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union` during colcon build of a Python node using this library.
  Using the `Any` from the `typing` module fixed this issue.
  Yes, this problem does not occur with the typeguard version provided by apt (2.2.2), but could also occur if Ubuntu bumps that version or for other users with a newer local pip install of typeguard.
* Remove `my_parameter` from python template (`#146 <https://github.com/PickNikRobotics/generate_parameter_library/issues/146>`_)
* Contributors: Bruno-Pier, Christoph Fröhlich, Jan Gutsche, Matthias Schoepfer, Paul Gesel, agonzat

* fix Python runtime parameters bug (`#165 <https://github.com/PickNikRobotics/generate_parameter_library/issues/165>`_)
* markdown/rst: Support __map\_ and nested parameters (`#164 <https://github.com/PickNikRobotics/generate_parameter_library/issues/164>`_)
  * Support nested parameters and maps for RST
  * Add read_only info to RST template
  * Use map parameters for AutoDocumentation
  * Add test for markdown generation
  * Use jinja indentation instead of regex
  * Add dynamic_parameters also to DefaultConfig
  * Proper fromat of default yaml config
  * Proper format of the default yaml file
  * Fix imported function names
  * Add a jinja2 filter to create valid multiline c++ string literals
  * Handle empty strings for descriptions
* parse_yaml.py: keep the trailing newline (`#159 <https://github.com/PickNikRobotics/generate_parameter_library/issues/159>`_)
* Fix rolling CI (`#162 <https://github.com/PickNikRobotics/generate_parameter_library/issues/162>`_)
* parse_yaml.py: fix issue with typeguard (`#154 <https://github.com/PickNikRobotics/generate_parameter_library/issues/154>`_)
* Bugfixes on Python code generation (`#152 <https://github.com/PickNikRobotics/generate_parameter_library/issues/152>`_)
  * Fix raising of validation error
  * Fix inverse logic of 'unique' validator
* Fix sentence for size_lt (`#150 <https://github.com/PickNikRobotics/generate_parameter_library/issues/150>`_)
* Fix typeguard error (`#149 <https://github.com/PickNikRobotics/generate_parameter_library/issues/149>`_)
  For typeguard==3.0.2, `default_value: any` raised a `TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union` during colcon build of a Python node using this library.
  Using the `Any` from the `typing` module fixed this issue.
  Yes, this problem does not occur with the typeguard version provided by apt (2.2.2), but could also occur if Ubuntu bumps that version or for other users with a newer local pip install of typeguard.
* Remove `my_parameter` from python template (`#146 <https://github.com/PickNikRobotics/generate_parameter_library/issues/146>`_)
* Contributors: Bruno-Pier, Christoph Fröhlich, Jan Gutsche, Matthias Schoepfer, Paul Gesel, agonzat

0.3.6 (2023-07-31)
------------------

0.3.5 (2023-07-28)
------------------
* Remove documentation of deprecated validator functions (`#135 <https://github.com/PickNikRobotics/generate_parameter_library/issues/135>`_)
* Contributors: Tyler Weaver

0.3.4 (2023-07-24)
------------------
* Use node logger (`#132 <https://github.com/PickNikRobotics/generate_parameter_library/issues/132>`_)
* Fixed incorrect usage of fmt, causing compile errors (`#127 <https://github.com/PickNikRobotics/generate_parameter_library/issues/127>`_)
* Add pyyaml as dependency (`#123 <https://github.com/PickNikRobotics/generate_parameter_library/issues/123>`_)
* Fix Python install (`#122 <https://github.com/PickNikRobotics/generate_parameter_library/issues/122>`_)
* Use correct syntax highlighting (`#121 <https://github.com/PickNikRobotics/generate_parameter_library/issues/121>`_)
* ReST template (`#119 <https://github.com/PickNikRobotics/generate_parameter_library/issues/119>`_)
* Fix empty arguments case and add custom validator prompt (`#117 <https://github.com/PickNikRobotics/generate_parameter_library/issues/117>`_)
* Update markdown template (`#116 <https://github.com/PickNikRobotics/generate_parameter_library/issues/116>`_)
* Fix output in current folder (`#115 <https://github.com/PickNikRobotics/generate_parameter_library/issues/115>`_)
* Generate Markdown Docs for Parameters  (`#111 <https://github.com/PickNikRobotics/generate_parameter_library/issues/111>`_)
* Add Python support for generate_parameter_library (`#110 <https://github.com/PickNikRobotics/generate_parameter_library/issues/110>`_)
  Co-authored-by: Tyler Weaver <tyler@picknik.ai>
* Update .pre-commit-config.yaml (`#108 <https://github.com/PickNikRobotics/generate_parameter_library/issues/108>`_)
* Log when a parameter is set (`#106 <https://github.com/PickNikRobotics/generate_parameter_library/issues/106>`_)
* Contributors: Christoph Fröhlich, Paul Gesel, Tyler Weaver, mosfet80, sprenger120

0.3.3 (2023-04-13)
------------------
* Fix Parameter Descriptor Incorrectly Populating Range Constraints for size_lt and size_gt (`#105 <https://github.com/PickNikRobotics/generate_parameter_library/issues/105>`_)
* Contributors: Chance Cardona

0.3.2 (2023-04-12)
------------------
* Populate Range Constraints in Parameter Descriptors from Validation Functions (`#103 <https://github.com/PickNikRobotics/generate_parameter_library/issues/103>`_)
* Mark deprecated rsl method and propose alternative in the docs. (`#102 <https://github.com/PickNikRobotics/generate_parameter_library/issues/102>`_)
* Allow none type (`#99 <https://github.com/PickNikRobotics/generate_parameter_library/issues/99>`_)
* Fixed tests never failing although file not found (`#101 <https://github.com/PickNikRobotics/generate_parameter_library/issues/101>`_)
* Contributors: Chance Cardona, Dr. Denis, GuiHome

0.3.1 (2023-02-01)
------------------

0.3.0 (2022-11-15)
------------------
* Migrate from parameter_traits to RSL (take 2) (`#91 <https://github.com/PickNikRobotics/generate_parameter_library/issues/91>`_)
* Add missing dependency on PyYAML (`#89 <https://github.com/PickNikRobotics/generate_parameter_library/issues/89>`_)
* Contributors: Scott K Logan, Tyler Weaver

0.2.8 (2022-11-03)
------------------
* Use typing syntax which is compatible with Python 3.6 (`#87 <https://github.com/PickNikRobotics/generate_parameter_library/issues/87>`_)
* Use YAML loader which is compatible with PyYAML 3.12 (`#88 <https://github.com/PickNikRobotics/generate_parameter_library/issues/88>`_)
* Contributors: Scott K Logan

0.2.7 (2022-10-28)
------------------

0.2.6 (2022-09-28)
------------------
* Depend on python dependencies in package.xml (`#74 <https://github.com/PickNikRobotics/generate_parameter_library/issues/74>`_)
* Contributors: Tyler Weaver

0.2.5 (2022-09-20)
------------------
* 🈵 Support use of '_' in mapped parameters. (`#68 <https://github.com/PickNikRobotics/generate_parameter_library/issues/68>`_)
* Test validators and fix bugs (`#66 <https://github.com/PickNikRobotics/generate_parameter_library/issues/66>`_)
* Fix deadlock in update_dynamic_parameters (`#64 <https://github.com/PickNikRobotics/generate_parameter_library/issues/64>`_)
* Parameter prefix (`#55 <https://github.com/PickNikRobotics/generate_parameter_library/issues/55>`_)
* Fix example parameters (`#54 <https://github.com/PickNikRobotics/generate_parameter_library/issues/54>`_)
* Contributors: Denis Štogl, Paul Gesel, Tyler Weaver

0.2.4 (2022-08-19)
------------------
* INTEGER type (`#53 <https://github.com/PickNikRobotics/generate_parameter_library/issues/53>`_)
* 0.2.3
* Contributors: Tyler Weaver

0.2.3 (2022-08-05)
------------------

0.2.2 (2022-08-03)
------------------
* Add better error messages (`#48 <https://github.com/PickNikRobotics/generate_parameter_library/issues/48>`_)
* Lock mutex around modifying internal state of ParamListener (`#47 <https://github.com/PickNikRobotics/generate_parameter_library/issues/47>`_)
* Contributors: Paul Gesel, Tyler Weaver

0.2.1 (2022-08-02)
------------------
* Fix scientific notation (`#46 <https://github.com/PickNikRobotics/generate_parameter_library/issues/46>`_)
* Contributors: Paul Gesel

0.2.0 (2022-08-01)
------------------
* Create stack allocated struct (`#45 <https://github.com/PickNikRobotics/generate_parameter_library/issues/45>`_)
* Fixed length arrays (`#44 <https://github.com/PickNikRobotics/generate_parameter_library/issues/44>`_)
* Fixed size string no default bug (`#43 <https://github.com/PickNikRobotics/generate_parameter_library/issues/43>`_)
* Move fixed size string to parameter traits (`#42 <https://github.com/PickNikRobotics/generate_parameter_library/issues/42>`_)
* static OK to fix ODR errors (`#41 <https://github.com/PickNikRobotics/generate_parameter_library/issues/41>`_)
* Change package name (`#40 <https://github.com/PickNikRobotics/generate_parameter_library/issues/40>`_)
* parameter validators interface library (`#32 <https://github.com/PickNikRobotics/generate_parameter_library/issues/32>`_)
* Validate fixed length Strings (`#33 <https://github.com/PickNikRobotics/generate_parameter_library/issues/33>`_)
* Fixed size strings (`#29 <https://github.com/PickNikRobotics/generate_parameter_library/issues/29>`_)
* Use single namespace validators (`#26 <https://github.com/PickNikRobotics/generate_parameter_library/issues/26>`_)
* Validate strings and arrays for size (`#24 <https://github.com/PickNikRobotics/generate_parameter_library/issues/24>`_)
* Contributors: Paul Gesel, Tyler Weaver

0.1.0 (2022-07-27)
------------------
* Python to generate C++ ROS parameter library.
* Contributors: Paul Gesel, Tyler Weaver
