#!/usr/bin/env python3

# Copyright 2023 PickNik Inc.
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

from setuptools import find_packages
from setuptools import setup

package_name = 'generate_parameter_library_py'

setup(
    name=package_name,
    version='1.3.1',
    packages=find_packages(),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        (
            'share/' + package_name + '/test',
            ['generate_parameter_library_py/test/wrong_default_type.yaml'],
        ),
        (
            'share/' + package_name + '/test',
            ['generate_parameter_library_py/test/missing_type.yaml'],
        ),
        (
            'share/' + package_name + '/test',
            ['generate_parameter_library_py/test/invalid_syntax.yaml'],
        ),
        (
            'share/' + package_name + '/test',
            ['generate_parameter_library_py/test/invalid_parameter_type.yaml'],
        ),
        (
            'share/' + package_name + '/test',
            ['generate_parameter_library_py/test/conflicting_element_bounds.yaml'],
        ),
        (
            'share/' + package_name + '/test',
            [
                'generate_parameter_library_py/test/conflicting_scalar_bounds_with_bounds.yaml'
            ],
        ),
        (
            'share/' + package_name + '/test',
            ['generate_parameter_library_py/test/valid_parameters.yaml'],
        ),
        (
            'share/' + package_name + '/test',
            ['generate_parameter_library_py/test/valid_parameters_with_none_type.yaml'],
        ),
        (
            'share/' + package_name + '/test',
            ['generate_parameter_library_py/test/nested_map_test.yaml'],
        ),
        (
            'share/' + package_name + '/test',
            ['generate_parameter_library_py/test/nested_map_keys.yaml'],
        ),
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ],
    install_requires=['setuptools', 'typeguard', 'jinja2', 'pyyaml'],
    package_data={
        '': [
            'jinja_templates/cpp/declare_parameter',
            'jinja_templates/cpp/declare_runtime_parameter',
            'jinja_templates/cpp/declare_struct',
            'jinja_templates/cpp/declare_variable',
            'jinja_templates/cpp/parameter_library_header',
            'jinja_templates/cpp/parameter_validation',
            'jinja_templates/cpp/remove_runtime_parameter',
            'jinja_templates/cpp/set_parameter',
            'jinja_templates/cpp/set_runtime_parameter',
            'jinja_templates/cpp/set_stack_params',
            'jinja_templates/cpp/update_parameter',
            'jinja_templates/cpp/update_runtime_parameter',
            'jinja_templates/markdown/default_config',
            'jinja_templates/markdown/documentation',
            'jinja_templates/markdown/parameter_detail',
            'jinja_templates/rst/default_config',
            'jinja_templates/rst/documentation',
            'jinja_templates/rst/parameter_detail',
            'jinja_templates/python/declare_parameter',
            'jinja_templates/python/declare_runtime_parameter',
            'jinja_templates/python/declare_struct',
            'jinja_templates/python/declare_variable',
            'jinja_templates/python/parameter_library_header',
            'jinja_templates/python/parameter_validation',
            'jinja_templates/python/remove_runtime_parameter',
            'jinja_templates/python/set_parameter',
            'jinja_templates/python/set_runtime_parameter',
            'jinja_templates/python/set_stack_params',
            'jinja_templates/python/update_parameter',
            'jinja_templates/python/update_runtime_parameter',
        ]
    },
    zip_safe=False,
    author='Paul Gesel',
    author_email='paul.gesel@picknik.ai',
    url='https://github.com/PickNikRobotics/generate_parameter_library',
    download_url='https://github.com/PickNikRobotics/generate_parameter_library/releases',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Generate the ROS parameter struct in C++ and Python with callbacks for updating.',
    license='BSD-3-Clause',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'generate_parameter_library_cpp = generate_parameter_library_py.generate_cpp_header:main',
            'generate_parameter_library_python = generate_parameter_library_py.generate_python_module:main',
            'generate_parameter_library_markdown = generate_parameter_library_py.generate_markdown:main',
            'generate_parameter_library_validate = generate_parameter_library_py.validate_config:main',
        ],
    },
)
