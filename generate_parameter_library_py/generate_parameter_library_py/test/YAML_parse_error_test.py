# Copyright 2022 PickNik, Inc.
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

import pytest
from unittest.mock import patch
import sys
import os

from ament_index_python.packages import get_package_share_path
from generate_parameter_library_py.generate_cpp_header import run as run_cpp
from generate_parameter_library_py.generate_python_module import run as run_python
from generate_parameter_library_py.generate_markdown import run as run_md
from generate_parameter_library_py.parse_yaml import (
    YAMLSyntaxError,
    validate_validator_combinations,
    preprocess_inputs,
)
from generate_parameter_library_py.generate_cpp_header import parse_args


def set_up(yaml_test_file):
    full_file_path = os.path.join(
        get_package_share_path('generate_parameter_library_py'), 'test', yaml_test_file
    )
    testargs = [sys.argv[0], '/tmp/' + yaml_test_file + '.h', full_file_path]

    with patch.object(sys, 'argv', testargs):
        args = parse_args()
        output_file = args.output_cpp_header_file
        yaml_file = args.input_yaml_file
        validate_header = args.validate_header
        run_cpp(output_file, yaml_file, validate_header)

    testargs = [sys.argv[0], '/tmp/' + yaml_test_file + '.py', full_file_path]

    with patch.object(sys, 'argv', testargs):
        args = parse_args()
        output_file = args.output_cpp_header_file
        yaml_file = args.input_yaml_file
        validate_header = args.validate_header
        run_python(output_file, yaml_file, validate_header)

    testargs = [sys.argv[0], '/tmp/' + yaml_test_file + '.md', full_file_path]

    with patch.object(sys, 'argv', testargs):
        args = parse_args()
        output_file = args.output_cpp_header_file
        yaml_file = args.input_yaml_file
        run_md(yaml_file, output_file, 'markdown')

    testargs = [sys.argv[0], '/tmp/' + yaml_test_file + '.rst', full_file_path]

    with patch.object(sys, 'argv', testargs):
        args = parse_args()
        output_file = args.output_cpp_header_file
        yaml_file = args.input_yaml_file
        run_md(yaml_file, output_file, 'rst')


# class TestViewValidCodeGen(unittest.TestCase):
@pytest.mark.parametrize(
    'test_input,expected',
    [
        (file_name, YAMLSyntaxError)
        for file_name in [
            'wrong_default_type.yaml',
            'missing_type.yaml',
            'invalid_syntax.yaml',
            'invalid_parameter_type.yaml',
            'conflicting_element_bounds.yaml',
            'conflicting_scalar_bounds_with_bounds.yaml',
        ]
    ],
)
def test_expected(test_input, expected):
    with pytest.raises(expected) as e:
        yaml_test_file = test_input
        set_up(yaml_test_file)
    print(e.value)


@pytest.mark.parametrize(
    'yaml_test_file',
    [
        ('valid_parameters.yaml'),
        ('valid_parameters_with_none_type.yaml'),
        ('nested_map_test.yaml'),
        ('nested_map_keys.yaml'),
    ],
)
def test_parse_valid_parameter_files(yaml_test_file):
    try:
        set_up(yaml_test_file)
    except Exception as e:
        assert False, f'failed to parse valid file, reason:{e}'


@pytest.mark.parametrize(
    'defined_type,validations,expected_message',
    [
        (
            'double_array',
            {'bounds<>': [0.0, 1.0]},
            'uses a scalar bound validator',
        ),
        (
            'int_array_fixed_03',
            {'gt_eq<>': [0]},
            'uses a scalar bound validator',
        ),
        (
            'double',
            {'element_bounds<>': [0.0, 1.0]},
            'uses an element bound validator',
        ),
        (
            'int',
            {'upper_element_bounds<>': [10]},
            'uses an element bound validator',
        ),
    ],
)
def test_bound_validator_matches_parameter_type(
    defined_type, validations, expected_message
):
    with pytest.raises(YAMLSyntaxError, match=expected_message):
        validate_validator_combinations('test_param', defined_type, validations)


@pytest.mark.parametrize(
    'defined_type,validations',
    [
        ('double_array', {'element_bounds<>': [0.0, 1.0]}),
        ('int_array_fixed_03', {'lower_element_bounds<>': [0]}),
        ('double', {'bounds<>': [0.0, 1.0]}),
        ('int', {'gt_eq<>': [0]}),
    ],
)
def test_bound_validator_accepts_matching_parameter_type(defined_type, validations):
    validate_validator_combinations('test_param', defined_type, validations)


@pytest.mark.parametrize(
    'defined_type,default_value',
    [
        ('int_array_fixed_03', [101, 102, 103, 104]),
        ('double_array_fixed_03', [1.0, 2.0, 3.0, 4.0]),
        ('string_array_fixed_03', ['a', 'b', 'c', 'd']),
        ('string_fixed_03', 'abcd'),
    ],
)
def test_fixed_default_cannot_exceed_capacity(defined_type, default_value):
    with pytest.raises(YAMLSyntaxError, match='exceeds the capacity'):
        preprocess_inputs(
            'cpp',
            'test_param',
            {'type': defined_type, 'default_value': default_value},
            ['test_namespace'],
        )


def test_fixed_default_must_satisfy_fixed_size_validator():
    with pytest.raises(YAMLSyntaxError, match="'fixed_size' validation requires 3"):
        preprocess_inputs(
            'cpp',
            'test_param',
            {
                'type': 'int_array_fixed_03',
                'default_value': [101, 102],
                'validation': {'fixed_size<>': 3},
            },
            ['test_namespace'],
        )


@pytest.mark.parametrize('default_value', [[101, 102], [101, 102, 103]])
def test_fixed_default_at_or_below_capacity_is_valid(default_value):
    preprocess_inputs(
        'cpp',
        'test_param',
        {'type': 'int_array_fixed_03', 'default_value': default_value},
        ['test_namespace'],
    )
