# Copyright 2026 Generate Parameter Library Contributors
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
#    * Neither the name of the Generate Parameter Library contributors nor
#      the names of its contributors may be used to endorse or promote
#      products derived from this software without specific prior written
#      permission.
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

"""Code generation and definition checks for `type: enum` parameters."""

import pytest

from generate_parameter_library_py.generate_cpp_header import run as run_cpp
from generate_parameter_library_py.generate_markdown import run as run_markdown
from generate_parameter_library_py.generate_python_module import run as run_python
from generate_parameter_library_py.parse_yaml import GenerateCode, YAMLSyntaxError
from generate_parameter_library_py.validate_config import validate

DEFINITION = """\
test_params:
  control_mode:
    type: enum
    enum_values: [position, velocity, effort]
    default_value: position
    description: "control mode"
  required_mode:
    type: enum
    enum_values: [fast, slow]
  pid:
    mode:
      type: enum
      enum_values: [p, pi, pid]
      default_value: pi
"""


def generate(tmp_path, run, output_name, definition=DEFINITION):
    yaml_file = tmp_path / 'params.yaml'
    yaml_file.write_text(definition)
    output_file = tmp_path / output_name
    run(str(output_file), str(yaml_file))
    return output_file.read_text()


def parse(tmp_path, language, parameter):
    """Parse a definition holding one parameter: its name, then its fields."""
    text = f'test_params:\n  {parameter[0]}:\n'
    text += ''.join(f'    {line}\n' for line in parameter[1:])
    definition = tmp_path / 'params.yaml'
    definition.write_text(text)
    GenerateCode(language).parse(str(definition), '')


def test_cpp_header_declares_enum_class_and_conversions(tmp_path):
    header = generate(tmp_path, run_cpp, 'params.hpp')

    assert 'enum class ControlMode {' in header
    # C++ names the enum from the global namespace, which no nested type hides
    control_mode = '::test_params::Params::ControlMode'
    assert f'{control_mode} control_mode = {control_mode}::position;' in header
    assert '::test_params::Params::RequiredMode required_mode;' in header
    # a nested enum is declared in its group and named through it
    mode = '::test_params::Params::Pid::Mode'
    assert 'enum class Mode {' in header
    assert f'{mode} mode = {mode}::pi;' in header
    # the ROS parameter stays a string
    assert 'auto parameter = rclcpp::ParameterType::PARAMETER_STRING;' in header
    assert 'auto parameter = to_parameter_value(updated_params.control_mode);' in header
    assert 'one_of<std::string>(param, {"position", "velocity", "effort"})' in header
    assert (
        f'updated_params.control_mode = from_string<{control_mode}>(param.as_string());'
        in header
    )
    assert (
        f'updated_params.pid.mode = from_string<{mode}>(param.as_string());' in header
    )
    assert f'inline std::string to_string({control_mode} value) {{' in header
    assert f'case {control_mode}::velocity:' in header
    assert f'inline auto to_parameter_value({mode} value) {{' in header
    # StackParams holds the enum declared in Params
    stack_params = header[header.index('struct StackParams {') :]
    assert 'output.control_mode = params.control_mode;' in header
    assert 'enum class' not in stack_params


def test_cpp_header_without_enums_has_no_conversions(tmp_path):
    header = generate(
        tmp_path,
        run_cpp,
        'params.hpp',
        'test_params:\n  mode:\n    type: string\n    default_value: "a"\n',
    )

    assert 'from_string' not in header
    assert 'enum class' not in header


def test_cpp_validation_on_enum_runs_after_one_of(tmp_path):
    header = generate(
        tmp_path,
        run_cpp,
        'params.hpp',
        DEFINITION
        + '  checked:\n'
        + '    type: enum\n'
        + '    enum_values: [a, b]\n'
        + '    validation:\n'
        + '      "custom_validators::check": null\n',
    )

    update = header[header.index('(prefix_ + "checked")') :]
    assert update.index('one_of<std::string>') < update.index(
        'custom_validators::check'
    )


def test_python_module_declares_str_enum(tmp_path):
    module = generate(tmp_path, run_python, 'params.py')

    assert 'import enum' in module
    assert 'class ControlMode(str, enum.Enum):' in module
    assert 'position = "position"' in module
    assert 'self.control_mode = self.ControlMode.position' in module
    assert 'self.required_mode = None' in module
    assert 'class Mode(str, enum.Enum):' in module
    assert 'self.mode = self.Mode.pi' in module
    # declare_parameter gets the string value of the default
    assert 'parameter = updated_params.control_mode.value' in module
    assert (
        'ParameterValidators.one_of(param, ["position", "velocity", "effort"])'
        in module
    )
    assert (
        'updated_params.control_mode = updated_params.ControlMode(param.value)'
        in module
    )
    assert 'updated_params.pid.mode = updated_params.pid.Mode(param.value)' in module
    compile(module, 'params.py', 'exec')


def test_markdown_documents_enum_as_string_with_allowed_values(tmp_path):
    yaml_file = tmp_path / 'params.yaml'
    yaml_file.write_text(DEFINITION)
    output_file = tmp_path / 'params.md'
    run_markdown(str(yaml_file), str(output_file), 'markdown')
    docs = output_file.read_text()

    assert '* Type: `enum`' in docs
    assert '* Default Value: "position"' in docs
    assert "one of the specified values: ['position', 'velocity', 'effort']" in docs


def test_validate_config_checks_enum_values(tmp_path):
    definition = tmp_path / 'definition.yaml'
    definition.write_text(DEFINITION)
    config = tmp_path / 'config.yaml'
    config.write_text(
        'test_params:\n'
        '  ros__parameters:\n'
        '    control_mode: torque\n'
        '    required_mode: fast\n'
    )

    diagnostics = validate([str(definition)], [str(config)])
    errors = [d.location for d in diagnostics if d.severity == 'ERROR']
    assert errors == ['test_params.control_mode']


@pytest.mark.parametrize('language', ['cpp', 'python'])
@pytest.mark.parametrize(
    'parameter,message',
    [
        (['mode', 'type: enum'], "needs 'enum_values'"),
        (['mode', 'type: enum', 'enum_values: []'], "needs 'enum_values'"),
        (['mode', 'type: enum', 'enum_values: fast'], "needs 'enum_values'"),
        (
            ['mode', 'type: enum', 'enum_values: [fast, slow, fast]'],
            "lists fast more than once in 'enum_values'",
        ),
        (
            [
                'mode',
                'type: enum',
                'enum_values: [fast, slow]',
                'default_value: medium',
            ],
            "default value 'medium', which is not one of its 'enum_values'",
        ),
        (
            ['mode', 'type: enum', 'enum_values: [fast, slow]', 'default_value: 1'],
            'incorrect type',
        ),
        (
            [
                'mode',
                'type: enum',
                'enum_values: [fast, slow]',
                'validation:',
                '  one_of<>: [[fast, slow]]',
            ],
            "Remove the 'one_of' validation",
        ),
        (['mode', 'type: enum', 'enum_values: [fast, 2nd]'], 'not a valid identifier'),
        (['mode', 'type: enum', 'enum_values: [fast, a-b]'], 'not a valid identifier'),
        # unquoted on/off/yes/no/true/false are YAML booleans
        (
            ['mode', 'type: enum', 'enum_values: [off, on]'],
            "False .* quote it, e.g. 'on'",
        ),
        (
            ['mode', 'type: enum', 'enum_values: [fast, yes]'],
            "True .* quote it, e.g. 'on'",
        ),
        (
            ['mode', 'type: enum', "enum_values: ['off', 'on']", 'default_value: off'],
            "default value False, a boolean. .* quote it, e.g. 'on'",
        ),
        (['mode', 'type: enum', 'enum_values: [fast, "é"]'], 'not a valid identifier'),
        (['mode', 'type: enum', 'enum_values: [fast, delete]'], 'keyword'),
        (['mode', 'type: enum', 'enum_values: [fast, and]'], 'keyword'),
        (['mode', 'type: enum', 'enum_values: [fast, lambda]'], 'keyword'),
        (['mode', 'type: enum', 'enum_values: [fast, None]'], 'keyword'),
        (['mode', 'type: enum', 'enum_values: [fast, _slow_]'], "reserved by Python's"),
        (['mode', 'type: enum', 'enum_values: [fast, mro]'], "reserved by Python's"),
        (
            ['mode', 'type: string', 'enum_values: [fast, slow]'],
            "'enum_values' is only valid for type 'enum'",
        ),
    ],
)
def test_invalid_enum_definition_is_a_syntax_error(
    tmp_path, language, parameter, message
):
    with pytest.raises(YAMLSyntaxError, match=message):
        parse(tmp_path, language, parameter)


@pytest.mark.parametrize('language', ['cpp', 'python'])
@pytest.mark.parametrize(
    'definition,message',
    [
        # the root parameters are fields of Params
        (
            'test_params:\n  params:\n    type: enum\n    enum_values: [a]\n',
            'inside the struct of the same name',
        ),
        (
            'test_params:\n'
            '  pid_gains:\n'
            '    pid_gains:\n'
            '      type: enum\n'
            '      enum_values: [a]\n',
            'inside the struct of the same name',
        ),
        (
            'test_params:\n'
            '  mode:\n'
            '    type: enum\n'
            '    enum_values: [a]\n'
            '  Mode:\n'
            '    type: int\n'
            '    default_value: 1\n',
            'which another member of its struct already uses',
        ),
        (
            'test_params:\n'
            '  control__mode:\n'
            '    gain:\n'
            '      type: double\n'
            '  control_mode:\n'
            '    type: enum\n'
            '    enum_values: [a]\n',
            'which another member of its struct already uses',
        ),
        # an enum named Params inside a group would hide the root Params struct
        (
            'test_params:\n'
            '  pid:\n'
            '    params:\n'
            '      type: enum\n'
            '      enum_values: [a]\n',
            'would hide the Params struct',
        ),
        # Python would set the group as an attribute that masks the enum class
        (
            'test_params:\n'
            '  control_mode:\n'
            '    type: enum\n'
            '    enum_values: [a]\n'
            '  ControlMode:\n'
            '    gain:\n'
            '      type: double\n',
            'which another member of its struct already uses',
        ),
        # None, True and False are Python keywords
        (
            'test_params:\n  none:\n    type: enum\n    enum_values: [a]\n',
            "type 'None', which is not a valid type name",
        ),
        (
            "test_params:\n  'true':\n    type: enum\n    enum_values: [a]\n",
            "type 'True', which is not a valid type name",
        ),
        (
            'test_params:\n'
            '  pid:\n'
            "    'false':\n"
            '      type: enum\n'
            '      enum_values: [a]\n',
            "type 'False', which is not a valid type name",
        ),
        (
            'test_params:\n'
            '  joints:\n'
            '    type: string_array\n'
            '    default_value: [a]\n'
            '  __map_joints:\n'
            '    mode:\n'
            '      type: enum\n'
            '      enum_values: [a]\n',
            'not supported for mapped parameters',
        ),
    ],
)
def test_enum_type_name_clashes(tmp_path, language, definition, message):
    yaml_file = tmp_path / 'params.yaml'
    yaml_file.write_text(definition)
    with pytest.raises(YAMLSyntaxError, match=message):
        GenerateCode(language).parse(str(yaml_file), '')


def test_group_named_params_does_not_hide_the_enum_type(tmp_path):
    """A nested struct named Params used to hide the root of the C++ type name."""
    header = generate(
        tmp_path,
        run_cpp,
        'params.hpp',
        'test_params:\n'
        '  pid:\n'
        '    mode:\n'
        '      type: enum\n'
        '      enum_values: [a, b]\n'
        '      default_value: a\n'
        '    params:\n'
        '      gain:\n'
        '        type: double\n'
        '        default_value: 1.0\n',
    )

    assert 'struct Params {' in header.split('struct Pid {')[1]
    mode = '::test_params::Params::Pid::Mode'
    assert f'{mode} mode = {mode}::a;' in header
