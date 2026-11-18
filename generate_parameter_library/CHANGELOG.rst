^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package generate_parameter_library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.4.0 (2026-11-17)
------------------
* Install parameter definitions to share/<package>/parameter_definitions (`#419 <https://github.com/ros-tooling/generate_parameter_library/issues/419>`_)
* Remove dead code (`#412 <https://github.com/ros-tooling/generate_parameter_library/issues/412>`_)
* Contributors: Christoph Fröhlich

1.3.1 (2026-10-05)
------------------

1.3.0 (2026-07-24)
------------------

1.2.0 (2026-06-09)
------------------

1.1.0 (2026-05-14)
------------------
* Remove tl_expected (`#355 <https://github.com/ros-tooling/generate_parameter_library/issues/355>`_)
* Contributors: Christoph Fröhlich

1.0.1 (2026-05-06)
------------------
* Silence deprecation warning for tl_expected (`#350 <https://github.com/ros-tooling/generate_parameter_library/issues/350>`_)
* Contributors: Christoph Fröhlich

1.0.0 (2026-04-22)
------------------
* Add repository README.md to generate_parameter_library package docs (`#296 <https://github.com/ros-tooling/generate_parameter_library/issues/296>`_)
* Remove deprecated parameter_traits (`#294 <https://github.com/ros-tooling/generate_parameter_library/issues/294>`_) (`#330 <https://github.com/ros-tooling/generate_parameter_library/issues/330>`_)
* Remove installation to deprecated include path (`#319 <https://github.com/ros-tooling/generate_parameter_library/issues/319>`_)
* Contributors: Christoph Fröhlich, Jonas Otto

0.8.0 (2026-03-22)
------------------
* Use libexpected-dev instead of tl_expected (`#322 <https://github.com/ros-tooling/generate_parameter_library/issues/322>`_)
* Contributors: Christoph Fröhlich

0.7.0 (2026-02-22)
------------------
* Use a temporary build directory for Python module output (`#303 <https://github.com/ros-tooling/generate_parameter_library/issues/303>`_)
* Move linters to pre-commit (`#298 <https://github.com/ros-tooling/generate_parameter_library/issues/298>`_)
* Contributors: Błażej Sowa, Christoph Fröhlich

0.6.0 (2025-12-06)
------------------
* Update maintainers for GBP release team (`#282 <https://github.com/ros-tooling/generate_parameter_library/issues/282>`_)
* Contributors: Nathan Brooks

0.5.0 (2025-06-12)
------------------
* Fix generate_parameter_library macro on Windows (`#242 <https://github.com/ros-tooling/generate_parameter_library/issues/242>`_)
* Contributors: Nathan Brooks, Silvio Traversaro

0.4.0 (2025-01-13)
------------------
* Change header install path (`#213 <https://github.com/ros-tooling/generate_parameter_library/issues/213>`_)
* Contributors: Auguste Bourgois

0.3.9 (2024-10-27)
------------------
* Disable cache for program (`#218 <https://github.com/ros-tooling/generate_parameter_library/issues/218>`_)
* Contributors: Paul Gesel

0.3.8 (2024-03-27)
------------------
* use python_install_dir (`#178 <https://github.com/ros-tooling/generate_parameter_library/issues/178>`_)
* Update CMakeLists.txt (`#173 <https://github.com/ros-tooling/generate_parameter_library/issues/173>`_)
* Contributors: Christoph Fröhlich, Paul Gesel

0.3.7 (2024-01-12)
------------------
* Enable generate_parameter_module through ament_cmake_python (`#161 <https://github.com/ros-tooling/generate_parameter_library/issues/161>`_)
* Contributors: Paul Gesel

0.3.6 (2023-07-31)
------------------

0.3.5 (2023-07-28)
------------------

0.3.4 (2023-07-24)
------------------
* Add Python support for generate_parameter_library (`#110 <https://github.com/ros-tooling/generate_parameter_library/issues/110>`_)
  Co-authored-by: Tyler Weaver <tyler@picknik.ai>
* Contributors: Paul Gesel

0.3.3 (2023-04-13)
------------------

0.3.2 (2023-04-12)
------------------

0.3.1 (2023-02-01)
------------------
* Add keyword INTERFACE to fix build error 'ar: no archive members specified' since the generated target is header-only (`#93 <https://github.com/ros-tooling/generate_parameter_library/issues/93>`_)
* Make it easy for users to override (`#92 <https://github.com/ros-tooling/generate_parameter_library/issues/92>`_)
* Contributors: Tyler Weaver, light-tech

0.3.0 (2022-11-15)
------------------
* Migrate from parameter_traits to RSL (take 2) (`#91 <https://github.com/ros-tooling/generate_parameter_library/issues/91>`_)
* Contributors: Tyler Weaver

0.2.8 (2022-11-03)
------------------

0.2.7 (2022-10-28)
------------------
* Standardize cmake (`#79 <https://github.com/ros-tooling/generate_parameter_library/issues/79>`_)
* Contributors: Tyler Weaver

0.2.6 (2022-09-28)
------------------
* Depend on python package (`#75 <https://github.com/ros-tooling/generate_parameter_library/issues/75>`_)
* Drop requirement for CMake to 3.16 (`#73 <https://github.com/ros-tooling/generate_parameter_library/issues/73>`_)
* Added -- for ros-args to find (`#71 <https://github.com/ros-tooling/generate_parameter_library/issues/71>`_)
* Contributors: Michael Wrock, Tyler Weaver

0.2.5 (2022-09-20)
------------------
* 🚀 Add cmake macros for using tests with example yaml files. 🤖 (`#57 <https://github.com/ros-tooling/generate_parameter_library/issues/57>`_)
  Co-authored-by: Tyler Weaver <maybe@tylerjw.dev>
* Contributors: Denis Štogl

0.2.4 (2022-08-19)
------------------
* 0.2.3
* Contributors: Tyler Weaver

0.2.3 (2022-08-05)
------------------

0.2.2 (2022-08-03)
------------------

0.2.1 (2022-08-02)
------------------

0.2.0 (2022-08-01)
------------------
* Fixed length arrays (`#44 <https://github.com/ros-tooling/generate_parameter_library/issues/44>`_)
* Change package name (`#40 <https://github.com/ros-tooling/generate_parameter_library/issues/40>`_)
* Cleaup cmake paths (`#38 <https://github.com/ros-tooling/generate_parameter_library/issues/38>`_)
* parameter validators interface library (`#32 <https://github.com/ros-tooling/generate_parameter_library/issues/32>`_)
* Support exporting parameter libraries (`#28 <https://github.com/ros-tooling/generate_parameter_library/issues/28>`_)
* Contributors: Paul Gesel, Tyler Weaver

0.1.0 (2022-07-27)
------------------
* CMake to generate ROS parameter library.
* Contributors: Paul Gesel, Tyler Weaver
