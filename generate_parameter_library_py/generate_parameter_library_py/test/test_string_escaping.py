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

"""Text values in a parameter definition must survive code generation unchanged."""

import ast
import json
import re

from generate_parameter_library_py.generate_cpp_header import run as run_cpp
from generate_parameter_library_py.generate_python_module import run as run_python

PATH = 'C:\\new "dir"'
NAMES = ['say "hi"', 'back\\slash']

DEFINITION = r"""
escaping_test:
  path:
    type: string
    default_value: 'C:\new "dir"'
  names:
    type: string_array
    default_value: ['say "hi"', 'back\slash']
"""

# A C++ string literal with the escapes the generator emits has JSON syntax.
CPP_STRING = r'"(?:[^"\\]|\\.)*"'


def write_definition(tmp_path):
    definition = tmp_path / 'parameters.yaml'
    definition.write_text(DEFINITION)
    return str(definition)


def python_assignments(source):
    """Map each `self.<name> = <literal>` in the generated module to its value."""
    values = {}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Attribute):
            try:
                values[node.targets[0].attr] = ast.literal_eval(node.value)
            except ValueError:
                pass
    return values


def test_definition_holds_the_expected_text(tmp_path):
    import yaml

    document = yaml.safe_load(open(write_definition(tmp_path)))
    assert document['escaping_test']['path']['default_value'] == PATH
    assert document['escaping_test']['names']['default_value'] == NAMES


def test_python_module_keeps_text_defaults(tmp_path):
    output = tmp_path / 'escaping_test.py'
    run_python(str(output), write_definition(tmp_path), '')

    values = python_assignments(output.read_text())
    assert values['path'] == PATH
    assert values['names'] == NAMES


def test_cpp_header_keeps_text_defaults(tmp_path):
    output = tmp_path / 'escaping_test.hpp'
    run_cpp(str(output), write_definition(tmp_path), '')
    header = output.read_text()

    path = re.search(r'std::string path = (' + CPP_STRING + ');', header)
    assert path is not None, 'no complete string literal for path'
    assert json.loads(path.group(1)) == PATH

    names = re.search(
        r'std::vector<std::string> names = \{((?:' + CPP_STRING + r'(?:, )?)*)\};',
        header,
    )
    assert names is not None, 'no complete initializer for names'
    assert [json.loads(n) for n in re.findall(CPP_STRING, names.group(1))] == NAMES


DESCRIBED = r"""
escaping_test:
  path:
    type: string
    default_value: ''
    description: 'say "hi" and end with a backslash \'
    additional_constraints: 'match \d+ "digits"'
"""


def descriptor_texts(source):
    """Collect the description and additional_constraints the generated module sets."""
    texts = {}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == (
            'ParameterDescriptor'
        ):
            for keyword in node.keywords:
                if keyword.arg == 'description':
                    texts['description'] = ast.literal_eval(keyword.value)
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.targets[0], ast.Attribute)
            and node.targets[0].attr == 'additional_constraints'
        ):
            texts['additional_constraints'] = ast.literal_eval(node.value)
    return texts


def test_python_module_keeps_descriptions(tmp_path):
    definition = tmp_path / 'parameters.yaml'
    definition.write_text(DESCRIBED)
    output = tmp_path / 'escaping_test.py'
    run_python(str(output), str(definition), '')

    assert descriptor_texts(output.read_text()) == {
        'description': 'say "hi" and end with a backslash \\',
        'additional_constraints': 'match \\d+ "digits"',
    }
