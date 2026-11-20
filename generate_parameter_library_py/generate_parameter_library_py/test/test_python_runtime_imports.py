# Copyright 2026 Austrian Institute of Technology GmbH (AIT)
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

"""Generated Python modules only import what generate_parameter_library_runtime_py provides."""

import ast

from generate_parameter_library_py.generate_python_module import run as run_python

# What generate_parameter_library_runtime_py and the standard library provide.
RUNTIME_MODULES = {
    'copy',
    'generate_parameter_library_runtime_py',
    'rcl_interfaces',
    'rclpy',
    'sys',
}


def test_generated_module_imports_only_runtime_packages(tmp_path):
    definition = tmp_path / 'parameters.yaml'
    definition.write_text(
        'ns:\n  rate:\n    type: double\n    default_value: 1.0\n'
        '    validation:\n      gt<>: [0.0]\n'
    )
    output = tmp_path / 'params.py'
    run_python(str(output), str(definition))

    imported = set()
    for node in ast.walk(ast.parse(output.read_text())):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module.split('.')[0])

    assert imported <= RUNTIME_MODULES
