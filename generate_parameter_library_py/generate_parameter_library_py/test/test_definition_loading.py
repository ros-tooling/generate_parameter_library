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

"""Loading a parameter definition must not run code written into it."""

import pytest

from generate_parameter_library_py.parse_yaml import GenerateCode, YAMLSyntaxError


def test_python_tags_are_rejected_and_not_executed(tmp_path):
    marker = tmp_path / 'created_by_definition'
    definition = tmp_path / 'parameters.yaml'
    definition.write_text(
        'tagged:\n'
        '  name:\n'
        '    type: string\n'
        f'    default_value: !!python/object/apply:os.mkdir ["{marker}"]\n'
    )

    with pytest.raises(YAMLSyntaxError):
        GenerateCode('cpp').parse(str(definition), '')
    assert not marker.exists()
