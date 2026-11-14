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

"""A default_value of the wrong type is reported as a definition error."""

import pytest

from generate_parameter_library_py.parse_yaml import GenerateCode, YAMLSyntaxError


@pytest.mark.parametrize(
    'defined_type,default_value',
    [
        # A scalar or empty list for a string used to crash while building the message.
        ('string', '5'),
        ('string', '1.5'),
        ('string', '[]'),
        # YAML bools are Python ints, so they used to pass as numbers.
        ('int', 'true'),
        ('double', 'false'),
        ('int_array', '[1, true]'),
        ('double_array', '[true]'),
    ],
)
@pytest.mark.parametrize('language', ['cpp', 'python'])
def test_wrong_default_type_is_a_syntax_error(
    tmp_path, language, defined_type, default_value
):
    definition = tmp_path / 'parameters.yaml'
    definition.write_text(
        'typed:\n'
        '  value:\n'
        f'    type: {defined_type}\n'
        f'    default_value: {default_value}\n'
    )

    with pytest.raises(YAMLSyntaxError, match='incorrect type'):
        GenerateCode(language).parse(str(definition), '')
