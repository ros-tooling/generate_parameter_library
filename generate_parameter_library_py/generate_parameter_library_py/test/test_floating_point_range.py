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

"""Double bounds must be floats in the generated Python module.

On Humble, rcl_interfaces messages assert the field type, so an integer bound such as
`gt_eq<>: 0` on a double parameter raised an AssertionError when declaring it.
"""

import ast

from generate_parameter_library_py.generate_python_module import run as run_python

DEFINITION = """
float_bounds_test:
  ratio:
    type: double
    default_value: 1.0
    validation:
      gt_eq<>: 0
  joints:
    type: string_array
    default_value: [a]
  gains:
    __map_joints:
      p:
        type: double
        default_value: 1.0
        validation:
          bounds<>: [0, 10]
"""


def range_values(source):
    """Evaluate the right-hand side of every floating_point_range assignment."""
    values = []
    for node in ast.walk(ast.parse(source)):
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.targets[0], ast.Attribute)
            and node.targets[0].attr in ('from_value', 'to_value')
            and 'floating_point_range' in ast.unparse(node.targets[0])
        ):
            expression = ast.Expression(node.value)
            values.append(
                eval(compile(expression, '<range>', 'eval'), {'float': float})
            )
    return values


def test_double_bounds_are_floats(tmp_path):
    definition = tmp_path / 'parameters.yaml'
    definition.write_text(DEFINITION)
    output = tmp_path / 'float_bounds_test.py'
    run_python(str(output), str(definition), '')

    values = range_values(output.read_text())
    assert values
    assert all(type(value) is float for value in values), values
