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

"""A parameter is recognised by its fields, whatever order they are written in."""

import pytest

from generate_parameter_library_py.parse_yaml import GenerateCode, YAMLSyntaxError


def parse(tmp_path, text):
    definition = tmp_path / 'parameters.yaml'
    definition.write_text(text)
    generator = GenerateCode('cpp')
    generator.parse(str(definition), '')
    return generator


def declared(generator):
    return {
        declaration.parameter_name: declaration.code_gen_variable.defined_type
        for declaration in generator.declare_parameters
    }


def test_validation_written_before_type(tmp_path):
    generator = parse(
        tmp_path,
        'key_order:\n'
        '  rate:\n'
        '    validation:\n'
        '      gt<>: [0.0]\n'
        '    type: double\n'
        '    default_value: 1.0\n'
        '  group:\n'
        '    gain:\n'
        '      validation: {gt_eq<>: [0.0]}\n'
        '      type: double\n'
        '      default_value: 2.0\n',
    )

    assert declared(generator) == {'rate': 'double', 'group.gain': 'double'}


def test_group_containing_a_parameter_named_type(tmp_path):
    generator = parse(
        tmp_path,
        'key_order:\n' '  group:\n' '    type:\n' '      type: string\n',
    )

    assert declared(generator) == {'group.type': 'string'}


def test_empty_group_is_a_syntax_error(tmp_path):
    with pytest.raises(YAMLSyntaxError):
        parse(tmp_path, 'key_order:\n' '  group: {}\n')
