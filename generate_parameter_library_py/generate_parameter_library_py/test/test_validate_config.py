#!/usr/bin/env python3

# Copyright 2026 PickNik Inc.
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

import os
import tempfile

import pytest

from generate_parameter_library_py.validate_config import main, validate

DEFINITION = """my_node:
  rate:
    type: double
    default_value: 10.0
    validation:
      gt<>: [0.0]
  name:
    type: string
    default_value: "robot"
  mandatory_gain:
    type: double
  mode:
    type: string
    default_value: "fast"
    validation:
      one_of<>: [["fast", "slow"]]
  joints:
    type: string_array
    default_value: ["a", "b"]
  offsets:
    type: double_array_fixed_2
    default_value: [0.0, 0.0]
  checked_by_cpp:
    type: int
    default_value: 3
    validation:
      "my_project::integer_equal_value": [3]
  enabled:
    type: bool
    default_value: true
  background:
    r:
      type: int
      default_value: 0
      validation:
        bounds<>: [0, 255]
"""

BAD_DEFAULT_DEFINITION = """default_node:
  items:
    type: string_array
    default_value: []
    validation:
      not_empty<>: null
  bad_number:
    type: double
    default_value: -1.0
    validation:
      gt<>: [0.0]
"""

MAPPED_DEFINITION = """mapped_node:
  joints:
    type: string_array
    default_value: ["shoulder", "elbow"]
  pid:
    __map_joints:
      p:
        type: double
        default_value: 1.0
        validation:
          gt<>: [0.0]
"""


def write(directory, name, text):
    path = os.path.join(directory, name)
    with open(path, 'w') as handle:
        handle.write(text)
    return path


@pytest.fixture
def workspace():
    with tempfile.TemporaryDirectory() as directory:
        yield directory


@pytest.fixture
def definition(workspace):
    return write(workspace, 'definition.yaml', DEFINITION)


def messages(diagnostics):
    return [str(diagnostic) for diagnostic in diagnostics]


def errors(diagnostics):
    return [d for d in diagnostics if d.severity == 'ERROR']


def test_valid_config_reports_nothing(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    rate: 20.0
    mandatory_gain: 1.5
    mode: "slow"
    background:
      r: 128
""",
    )
    assert validate([definition], [config]) == []


def test_missing_mandatory_parameter_is_an_error(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    rate: 20.0
""",
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert 'mandatory_gain' in found[0].location
    assert 'default_value' in found[0].message


def test_integer_for_a_double_is_reported(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    rate: 20
    mandatory_gain: 1.5
""",
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert 'my_node.rate' == found[0].location
    assert '20.0' in found[0].message


def test_wrong_scalar_type_is_reported(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    rate: "fast"
    mandatory_gain: 1.5
""",
    )
    found = errors(validate([definition], [config]))
    assert "expected type 'double', got a quoted 'string'" in found[0].message


def test_value_out_of_bounds_is_reported(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
    background:
      r: 300
""",
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert found[0].location == 'my_node.background.r'


def test_value_outside_one_of_is_reported(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
    mode: "medium"
""",
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert found[0].location == 'my_node.mode'


def test_array_element_type_is_checked(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
    joints: ["a", 2]
""",
    )
    found = errors(validate([definition], [config]))
    assert 'element 1 of the array' in found[0].message


def test_fixed_size_array_is_checked(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
    offsets: [0.0, 1.0, 2.0]
""",
    )
    found = errors(validate([definition], [config]))
    assert 'fixed size of 2' in found[0].message


def test_custom_cpp_validator_is_skipped_with_a_warning(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
    checked_by_cpp: 7
""",
    )
    diagnostics = validate([definition], [config])
    assert errors(diagnostics) == []
    assert [d.severity for d in diagnostics] == ['WARNING']
    assert 'my_project::integer_equal_value' in diagnostics[0].message


def test_unknown_parameter_is_reported_in_strict_mode_only(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
    background:
      colour: 1
""",
    )
    assert errors(validate([definition], [config])) == []
    found = errors(validate([definition], [config], strict=True))
    assert len(found) == 1
    assert found[0].location == 'my_node.background.colour'
    assert "did you mean 'background.r'" in found[0].message


def test_defaults_are_reported_in_strict_mode(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
""",
    )
    diagnostics = validate([definition], [config], strict=True)
    assert errors(diagnostics) == []
    assert any('will use default_value' in str(d) for d in diagnostics)


def test_wildcard_node_supplies_values(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """/**:
  ros__parameters:
    mandatory_gain: 1.5
my_node:
  ros__parameters:
    rate: 5.0
""",
    )
    assert validate([definition], [config]) == []


def test_plain_parameter_tree_without_ros_parameters(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """rate: 20.0
mandatory_gain: 1.5
""",
    )
    assert validate([definition], [config]) == []


def test_mapped_parameters_expand_from_the_config(workspace):
    definition = write(workspace, 'mapped.yaml', MAPPED_DEFINITION)
    config = write(
        workspace,
        'config.yaml',
        """mapped_node:
  ros__parameters:
    joints: ["shoulder", "wrist"]
    pid:
      shoulder:
        p: 2.0
      wrist:
        p: -1.0
""",
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert found[0].location == 'mapped_node.pid.wrist.p'


def test_several_definitions_match_by_namespace(workspace):
    first = write(workspace, 'first.yaml', DEFINITION)
    second = write(workspace, 'second.yaml', MAPPED_DEFINITION)
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
mapped_node:
  ros__parameters:
    joints: ["shoulder"]
    pid:
      shoulder:
        p: 2.0
""",
    )
    assert validate([first, second], [config]) == []


def test_validator_that_raises_is_a_warning(workspace, monkeypatch):
    """A validator we cannot evaluate must not be reported as a bad value."""
    from generate_parameter_library_py import validate_config

    def explode(param, *arguments):
        raise RuntimeError('boom')

    monkeypatch.setattr(
        validate_config.ParameterValidators, 'gt', explode, raising=True
    )
    definition = write(workspace, 'definition.yaml', DEFINITION)
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    rate: 20.0
    mandatory_gain: 1.5
""",
    )
    diagnostics = validate([definition], [config])
    assert errors(diagnostics) == []
    assert [d.severity for d in diagnostics] == ['WARNING']
    assert 'RuntimeError' in diagnostics[0].message


def test_unused_definitions_are_reported_and_not_parsed(workspace, definition):
    """A definition no section refers to is skipped, and the skip is visible."""
    broken = write(
        workspace,
        'broken.yaml',
        """other_node:
  bad:
    type: not_a_real_type
""",
    )
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
""",
    )
    diagnostics = validate([definition, broken], [config])
    assert errors(diagnostics) == []
    assert [d.severity for d in diagnostics] == ['WARNING']
    assert 'broken.yaml' in diagnostics[0].message


def test_wildcard_only_config_is_validated(workspace, definition):
    """A file whose only section is the wildcard still describes a node."""
    config = write(
        workspace,
        'config.yaml',
        """/**:
  ros__parameters:
    rate: -1.0
    mandatory_gain: 1.5
""",
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert 'rate' in found[0].location


def test_none_typed_parameters_are_left_alone(workspace):
    """A parameter of type none is declared by other code, not by the node."""
    definition = write(
        workspace,
        'none.yaml',
        """external_node:
  some_parameter:
    type: string
    default_value: "hello"
  some_external_parameter:
    type: none
""",
    )
    config = write(
        workspace,
        'config.yaml',
        """external_node:
  ros__parameters:
    some_parameter: "hello"
    some_external_parameter:
      filter1:
        type: "LowPass"
""",
    )
    assert validate([definition], [config], strict=True) == []


def test_mapped_keys_fall_back_to_the_declared_default(workspace):
    """The node expands a map over the effective key list, so the tool must."""
    definition = write(workspace, 'mapped.yaml', MAPPED_DEFINITION)
    config = write(
        workspace,
        'config.yaml',
        """mapped_node:
  ros__parameters:
    pid:
      shoulder:
        p: -2.0
      elbow:
        p: 3.0
""",
    )
    found = errors(validate([definition], [config], strict=True))
    assert len(found) == 1
    assert found[0].location == 'mapped_node.pid.shoulder.p'


def test_node_name_with_namespace_or_leading_slash_matches(workspace, definition):
    """A section may carry a leading slash or a namespace; a definition cannot."""
    other = write(workspace, 'other.yaml', MAPPED_DEFINITION)
    shapes = {
        'leading slash': (
            '/my_node:\n'
            '  ros__parameters:\n'
            '    rate: -5.0\n'
            '    mandatory_gain: 1.5\n'
        ),
        'namespace': (
            'my_ns:\n'
            '  my_node:\n'
            '    ros__parameters:\n'
            '      rate: -5.0\n'
            '      mandatory_gain: 1.5\n'
        ),
    }
    for shape, text in shapes.items():
        config = write(workspace, 'config.yaml', text)
        found = errors(validate([definition, other], [config]))
        assert len(found) == 1, shape
        assert 'rate' in found[0].location, shape


def test_built_in_parameters_are_not_unknown(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """/**:
  ros__parameters:
    use_sim_time: true
    mandatory_gain: 1.5
my_node:
  ros__parameters:
    rate: 5.0
""",
    )
    assert errors(validate([definition], [config], strict=True)) == []


def test_scientific_notation_is_a_double(workspace, definition):
    """ROS 2 reads 1e5 as a double even though PyYAML calls it a string."""
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    rate: 1e5
    mandatory_gain: 1e-3
""",
    )
    assert validate([definition], [config]) == []


def test_word_that_ros_reads_as_a_bool_is_an_error(workspace, definition):
    """ROS 2 reads a plain y as a bool, so a string parameter gets a bool."""
    config = write(
        workspace,
        'config.yaml',
        'my_node:\n  ros__parameters:\n    mandatory_gain: 1.5\n    name: y\n',
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert 'reads y as a bool' in found[0].message


def test_quoted_bool_word_stays_a_string(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        'my_node:\n  ros__parameters:\n    mandatory_gain: 1.5\n    name: "y"\n',
    )
    assert validate([definition], [config]) == []


def test_plain_bool_word_is_a_bool(workspace, definition):
    """ROS 2 reads a plain y as a bool, so a bool parameter accepts it."""
    config = write(
        workspace,
        'config.yaml',
        'my_node:\n  ros__parameters:\n    mandatory_gain: 1.5\n    enabled: y\n',
    )
    assert validate([definition], [config]) == []


def test_quoted_number_is_not_a_double(workspace, definition):
    """ROS 2 keeps a quoted scalar a string, so the node would reject it."""
    config = write(
        workspace,
        'config.yaml',
        'my_node:\n  ros__parameters:\n    rate: "2.0"\n    mandatory_gain: 1.5\n',
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert found[0].location == 'my_node.rate'
    assert 'quoted' in found[0].message


def test_quoted_scientific_notation_stays_a_string(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        'my_node:\n  ros__parameters:\n    rate: "1e5"\n    mandatory_gain: 1.5\n',
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert found[0].location == 'my_node.rate'


def test_quoted_number_element_is_not_a_double(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        'my_node:\n  ros__parameters:\n    mandatory_gain: 1.5\n    offsets: ["1.0", 2.0]\n',
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert 'element 0' in found[0].message


def test_invalid_default_is_reported_when_the_parameter_is_omitted(workspace):
    """The node validates the effective value, which is the default when omitted."""
    definition = write(workspace, 'definition.yaml', BAD_DEFAULT_DEFINITION)
    config = write(
        workspace,
        'config.yaml',
        'default_node:\n  ros__parameters: {}\n',
    )
    found = errors(validate([definition], [config]))
    assert {d.location for d in found} == {
        'default_node.items',
        'default_node.bad_number',
    }


def test_invalid_default_is_not_reported_when_the_config_sets_the_parameter(workspace):
    definition = write(workspace, 'definition.yaml', BAD_DEFAULT_DEFINITION)
    config = write(
        workspace,
        'config.yaml',
        'default_node:\n'
        '  ros__parameters:\n'
        '    items: ["a"]\n'
        '    bad_number: 1.0\n',
    )
    assert validate([definition], [config]) == []


def test_node_section_is_found_through_nested_namespaces(workspace, definition):
    """A node may sit under any number of namespace levels."""
    config = write(
        workspace,
        'config.yaml',
        'robot:\n'
        '  arm:\n'
        '    my_node:\n'
        '      ros__parameters:\n'
        '        rate: -5.0\n'
        '        mandatory_gain: 1.5\n',
    )
    found = errors(validate([definition], [config], strict=True))
    assert len(found) == 1
    assert found[0].location == 'robot/arm/my_node.rate'


def test_valid_config_in_a_nested_namespace_reports_nothing(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        'robot:\n'
        '  arm:\n'
        '    my_node:\n'
        '      ros__parameters:\n'
        '        rate: 20.0\n'
        '        mandatory_gain: 1.5\n',
    )
    assert validate([definition], [config]) == []


def test_later_section_wins_over_an_earlier_one(workspace, definition):
    """rclcpp applies matching sections in file order, wildcard or not."""
    config = write(
        workspace,
        'config.yaml',
        'my_node:\n'
        '  ros__parameters:\n'
        '    rate: 20.0\n'
        '    mandatory_gain: 1.5\n'
        '/**:\n'
        '  ros__parameters:\n'
        '    rate: -1.0\n',
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert found[0].location == 'my_node.rate'


def test_single_level_wildcards_match_like_rclcpp(workspace, definition):
    """/* stands for one level and /** for any number, anywhere in the name."""
    config = write(
        workspace,
        'config.yaml',
        '/*/arm/*:\n'
        '  ros__parameters:\n'
        '    mandatory_gain: 1.5\n'
        '/**/arm/my_node:\n'
        '  ros__parameters:\n'
        '    rate: -1.0\n'
        '/robot/arm/my_node:\n'
        '  ros__parameters:\n'
        '    name: "a"\n',
    )
    found = errors(validate([definition], [config]))
    assert {d.location for d in found} == {
        '/**/arm/my_node.rate',
        '/robot/arm/my_node.rate',
    }


def test_single_level_wildcard_does_not_reach_deeper_nodes(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        '/robot/*:\n'
        '  ros__parameters:\n'
        '    mandatory_gain: 1.5\n'
        '/robot/arm/my_node:\n'
        '  ros__parameters:\n'
        '    rate: 20.0\n',
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert found[0].location == '/robot/arm/my_node.mandatory_gain'


def test_spellings_of_one_node_are_merged(workspace, definition):
    """/ns/my_node and ns: {my_node: ...} name the same node."""
    config = write(
        workspace,
        'config.yaml',
        '/ns/my_node:\n'
        '  ros__parameters:\n'
        '    mandatory_gain: 1.5\n'
        'ns:\n'
        '  my_node:\n'
        '    ros__parameters:\n'
        '      rate: -1.0\n',
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert found[0].location == '/ns/my_node.rate'


def test_repeated_slash_in_a_node_name_is_rejected(workspace, definition):
    """rcl_yaml_param_parser refuses /ns: {/my_node: ...} and the whole file."""
    config = write(
        workspace,
        'config.yaml',
        '/ns:\n  /my_node:\n    ros__parameters:\n      mandatory_gain: 1.5\n',
    )
    assert main(['--param-definition', definition, '--config', config]) == 1


def test_bool_word_in_a_default_is_a_string(workspace):
    """A default_value is compiled into the node, not parsed as config text."""
    definition = write(
        workspace,
        'definition.yaml',
        'default_node:\n'
        '  axes:\n'
        '    type: string_array\n'
        '    default_value: ["x", "y", "rz"]\n',
    )
    config = write(
        workspace,
        'config.yaml',
        'default_node:\n  ros__parameters: {}\n',
    )
    assert validate([definition], [config]) == []


def test_empty_default_array_is_not_reported(workspace):
    """An empty default is compiled into the node, rcl never reads it."""
    definition = write(
        workspace,
        'definition.yaml',
        'default_node:\n'
        '  joints:\n'
        '    type: string_array\n'
        '    default_value: []\n',
    )
    config = write(
        workspace,
        'config.yaml',
        'default_node:\n  ros__parameters: {}\n',
    )
    assert validate([definition], [config]) == []


def test_integer_default_for_a_double_is_not_reported(workspace):
    """The generator converts an integer default_value of a double to 1.0."""
    definition = write(
        workspace,
        'definition.yaml',
        'default_node:\n'
        '  rate:\n'
        '    type: double\n'
        '    default_value: 1\n'
        '    validation:\n'
        '      gt<>: [0.0]\n'
        '  gains:\n'
        '    type: double_array\n'
        '    default_value: [1, 2]\n',
    )
    config = write(
        workspace,
        'config.yaml',
        'default_node:\n  ros__parameters: {}\n',
    )
    assert validate([definition], [config]) == []


def test_block_scalar_is_read_like_a_plain_scalar(workspace, definition):
    """rcl_yaml_param_parser only keeps single and double quoted scalars as text."""
    config = write(
        workspace,
        'config.yaml',
        'my_node:\n  ros__parameters:\n    rate: >-\n      2.0\n    mandatory_gain: 1.5\n',
    )
    assert validate([definition], [config]) == []


def test_empty_array_is_reported(workspace, definition):
    """ROS 2 cannot type an empty sequence and leaves the parameter unset."""
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
    joints: []
""",
    )
    found = errors(validate([definition], [config]))
    assert len(found) == 1
    assert 'PARAMETER_NOT_SET' in found[0].message


def test_duplicate_namespace_is_reported(workspace, definition):
    twin = write(
        workspace,
        'twin.yaml',
        """my_node:
  something_else:
    type: int
    default_value: 1
""",
    )
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
""",
    )
    found = errors(validate([definition, twin], [config]))
    assert any('declared by both' in d.message for d in found)


def test_one_definition_does_not_claim_unrelated_sections(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
some_other_node:
  ros__parameters:
    completely: "different"
""",
    )
    diagnostics = validate([definition], [config])
    assert errors(diagnostics) == []
    assert any('not checked' in d.message for d in diagnostics)


def test_missing_file_is_reported_without_a_traceback(workspace, definition):
    code = main(['--param-definition', definition, '--config', '/no/such/config.yaml'])
    assert code == 1


def test_main_returns_non_zero_on_error(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    rate: "fast"
    mandatory_gain: 1.5
""",
    )
    code = main(['--param-definition', definition, '--config', config])
    assert code == 1


def test_main_returns_zero_on_success(workspace, definition):
    config = write(
        workspace,
        'config.yaml',
        """my_node:
  ros__parameters:
    mandatory_gain: 1.5
""",
    )
    assert main(['--param-definition', definition, '--config', config]) == 0
