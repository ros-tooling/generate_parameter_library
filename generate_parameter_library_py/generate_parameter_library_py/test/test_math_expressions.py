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

import ast
import math

import pytest
import yaml

from generate_parameter_library_py.generate_cpp_header import run as run_cpp
from generate_parameter_library_py.generate_python_module import run as run_python
from generate_parameter_library_py.generate_markdown import run as run_docs
from generate_parameter_library_py.parse_yaml import (
    YAMLSyntaxError,
    evaluate_math,
    preprocess_inputs,
)


@pytest.mark.parametrize(
    'expression, expected',
    [
        ('${pi/2}', math.pi / 2),
        ('${ -tau + (+pi) * 2 }', 0.0),
        ('${e}', math.e),
        ('${(2 + 3) * 4 - 1}', 19),
        ('${7 // 2 + 7 % 2}', 4),
    ],
)
def test_arithmetic(expression, expected):
    assert evaluate_math(expression, 'angle') == expected


@pytest.mark.parametrize(
    'expression',
    [
        '${pi/0}',
        '${pi/}',
        '${pi',
        '${unknown}',
        '${1e309}',
        '${True}',
        '${1j}',
        '${pi.real}',
        '${[1][0]}',
        '${__import__("os").getcwd()}',
        '${2 ** 1000000000}',
    ],
)
def test_invalid_expression(expression):
    with pytest.raises(
        YAMLSyntaxError, match='Parameter angle has invalid math expression'
    ):
        evaluate_math(expression, 'angle')


@pytest.mark.parametrize('language', ['cpp', 'python', 'markdown', 'rst'])
@pytest.mark.parametrize('defined_type', ['int', 'int_array', 'int_array_fixed_3'])
def test_integer_expression_type_error(language, defined_type):
    value = '${pi/2}' if defined_type == 'int' else ['${pi/2}']
    with pytest.raises(YAMLSyntaxError, match='incorrect type'):
        preprocess_inputs(
            language, 'angle', {'type': defined_type, 'default_value': value}, ['test']
        )


@pytest.mark.parametrize('language', ['cpp', 'python', 'markdown', 'rst'])
@pytest.mark.parametrize('arguments', ['${1 + 1}', ['${1 + 1}']])
def test_fixed_size_validator_expression(language, arguments):
    definition = {
        'type': 'double_array_fixed_3',
        'default_value': ['${pi/2}'],
        'validation': {'fixed_size<>': arguments},
    }
    with pytest.raises(YAMLSyntaxError, match="'fixed_size' validation requires 2"):
        preprocess_inputs(language, 'angles', definition, ['test'])

    definition['default_value'].append('${-pi/2}')
    variable, *_ = preprocess_inputs(language, 'angles', definition, ['test'])
    assert variable.default_value == [math.pi / 2, -math.pi / 2]


@pytest.mark.parametrize('language', ['cpp', 'python', 'markdown', 'rst'])
def test_generated_math_matches_literal_values(tmp_path, language):
    parameters = {
        'max_angle': {
            'type': 'double',
            'default_value': '${pi/2}',
            'validation': {'bounds<>': ['${-pi}', '${pi}']},
        },
        'angles': {
            'type': 'double_array',
            'default_value': ['${pi}', '${tau/2}'],
            'validation': {'element_bounds<>': ['${-tau}', '${tau}']},
        },
        'fixed_angles': {'type': 'double_array_fixed_3', 'default_value': ['${pi/2}']},
        'count': {
            'type': 'int',
            'default_value': '${2 * 3}',
            'validation': {'one_of<>': [['${2 * 3}', 7]]},
        },
        'counts': {'type': 'int_array', 'default_value': ['${8 // 2}', 5]},
        'literal': {
            'type': 'string',
            'default_value': '${pi/2}',
            'description': 'Keep ${pi/2} as text',
        },
        'literals': {'type': 'string_array', 'default_value': ['${pi/2}']},
    }
    source = tmp_path / 'parameters.yaml'
    output = tmp_path / 'parameters.out'

    def generate():
        source.write_text(yaml.safe_dump({'test': parameters}))
        if language == 'cpp':
            run_cpp(str(output), str(source))
        elif language == 'python':
            run_python(str(output), str(source))
            ast.parse(output.read_text())
        else:
            run_docs(str(source), str(output), language)
        return output.read_text()

    expressions = generate()
    parameters['max_angle']['default_value'] = math.pi / 2
    parameters['max_angle']['validation']['bounds<>'] = [-math.pi, math.pi]
    parameters['angles']['default_value'] = [math.pi, math.pi]
    parameters['angles']['validation']['element_bounds<>'] = [-math.tau, math.tau]
    parameters['fixed_angles']['default_value'] = [math.pi / 2]
    parameters['count']['default_value'] = 6
    parameters['count']['validation']['one_of<>'] = [[6, 7]]
    parameters['counts']['default_value'] = [4, 5]
    assert expressions == generate()
    assert '${pi/2}' in expressions
