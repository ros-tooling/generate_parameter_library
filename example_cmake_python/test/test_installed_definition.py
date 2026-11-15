# Copyright 2026 ros2_control Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The parameter definition is installed, and validates a configuration."""

import filecmp
import os

from ament_index_python.packages import get_package_share_directory
from generate_parameter_library_py.validate_config import ERROR, validate

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALLED = os.path.join(
    get_package_share_directory('cmake_generate_parameter_module_example'),
    'parameter_definitions',
    'admittance_parameters.yaml',
)


def test_definition_is_installed():
    assert filecmp.cmp(
        INSTALLED,
        os.path.join(
            PACKAGE_DIR, 'cmake_generate_parameter_module_example/parameters.yaml'
        ),
        shallow=False,
    )


def test_installed_definition_validates_the_config():
    config = os.path.join(PACKAGE_DIR, 'config/implementation.yaml')
    diagnostics = validate([INSTALLED], [config])
    assert [d for d in diagnostics if d.severity == ERROR] == []
