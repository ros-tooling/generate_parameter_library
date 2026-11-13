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

"""Validate a ROS 2 parameter configuration file against parameter definitions.

This runs without a ROS 2 installation, a colcon workspace or a running node, so
it can be used as a CI step or by anyone who configures a robot from a laptop.
"""

import argparse
import difflib
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

from generate_parameter_library_py.parse_yaml import GenerateCode
from generate_parameter_library_py.python_validators import ParameterValidators

ROS_PARAMETERS_KEY = 'ros__parameters'
WILDCARD_NAMES = ('*', '**')
# Stands in for a wildcard level when matching sections against each other.
WILDCARD_STAND_IN = '__any__'

ERROR = 'ERROR'
WARNING = 'WARNING'

# Most unknown parameters for which a 'did you mean' suggestion is computed.
MAX_SUGGESTIONS = 10

# Parameters every node declares for itself, which no definition ever holds.
BUILT_IN_PARAMETERS = ('use_sim_time', 'start_type_description_service')
BUILT_IN_PREFIXES = ('qos_overrides.',)

# Words rcl_yaml_param_parser reads as a bool. PyYAML leaves the short ones as
# strings, so a string parameter given one of those gets a bool at runtime.
RCL_BOOL_WORDS = frozenset(
    'y Y yes Yes YES n N no No NO true True TRUE false False FALSE '
    'on On ON off Off OFF'.split()
)
RCL_TRUE_WORDS = frozenset('y yes true on'.split())


class Quoted(str):
    """Text that was written with quotes in the YAML source.

    ROS 2 keeps a quoted scalar a string whatever it contains, while the same
    text unquoted may be read as a number or a bool. Subclassing str keeps
    every consumer working; only the type check looks at the quoting. Block
    scalars (| and >) are not quoted: rcl_yaml_param_parser resolves their
    type like a plain scalar.
    """

    __slots__ = ()


QUOTED_STYLES = ("'", '"')


def _construct_scalar_text(loader, node):
    text = loader.construct_scalar(node)
    return Quoted(text) if node.style in QUOTED_STYLES else text


class ConfigLoader(yaml.SafeLoader):
    """A SafeLoader that remembers which scalars were written with quotes."""


ConfigLoader.add_constructor('tag:yaml.org,2002:str', _construct_scalar_text)


@dataclass
class Diagnostic:
    """One finding, printed as a single line."""

    severity: str
    location: str
    message: str

    def __str__(self):
        return f'{self.severity}: {self.location}: {self.message}'


class _ValidatorParam:
    """The duck type the validators in python_validators.py expect."""

    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value


class DeclaredParameter:
    """A parameter of a definition file, flattened to a dotted name."""

    def __init__(self, declaration, name: Optional[str] = None):
        variable = declaration.code_gen_variable
        self.name = name if name is not None else variable.param_name
        self.scalar_type = variable.defined_base_type
        self.is_array = variable.array_type
        self.fixed_size = variable.fixed_size
        self.default_value = variable.default_value
        self.validations = declaration.parameter_validations

    @property
    def has_default(self) -> bool:
        return self.default_value is not None


def yaml_type_name(value: Any) -> str:
    """Name the type of a value the way a definition file would spell it."""
    if isinstance(value, bool):
        return 'bool'
    if isinstance(value, int):
        return 'int'
    if isinstance(value, float):
        return 'double'
    if isinstance(value, str):
        return 'string'
    if isinstance(value, list):
        return 'array'
    if value is None:
        return 'null'
    return type(value).__name__


def reads_as_number(value: Any, expected: str) -> bool:
    """Would rcl_yaml_param_parser read this text as the expected number?

    PyYAML only resolves a float when the text has both a decimal point and a
    signed exponent, so '1e5' and '1e-3' arrive here as strings while ROS 2
    reads them as doubles. Quoted text is never a number: ROS 2 keeps a quoted
    scalar a string, whatever it contains.
    """
    if not isinstance(value, str) or isinstance(value, Quoted):
        return False
    try:
        if expected == 'int':
            int(value, 10)
        elif expected == 'double':
            float(value)
        else:
            return False
    except ValueError:
        return False
    return True


def reads_as_bool(value: Any) -> bool:
    """Would rcl_yaml_param_parser read this text as a bool?

    PyYAML resolves most of the YAML 1.1 bool words itself, so the only text
    that arrives here as a string is 'y' and 'n'. A quoted scalar is never a
    bool.
    """
    return (
        isinstance(value, str)
        and not isinstance(value, Quoted)
        and value in RCL_BOOL_WORDS
    )


def check_scalar_type(expected: str, value: Any) -> Optional[str]:
    actual = yaml_type_name(value)
    if actual == expected:
        return None
    if expected == 'bool' and reads_as_bool(value):
        # ROS 2 reads 'y' and 'n' as bools even though PyYAML calls them strings.
        return None
    if expected == 'double' and actual == 'int':
        return (
            f"expected type 'double', got 'int' ({value}); ROS 2 does not convert "
            f'integers to doubles, write {value}.0'
        )
    if isinstance(value, Quoted):
        return (
            f"expected type '{expected}', got a quoted '{actual}'; ROS 2 keeps "
            f'quoted scalars as strings'
        )
    if reads_as_number(value, expected):
        return None
    return f"expected type '{expected}', got '{actual}'"


def coerce_value(parameter: 'DeclaredParameter', value: Any) -> Any:
    """Read a scalar the way rcl_yaml_param_parser would before validating it.

    PyYAML leaves '1e5' as a string, so a validator such as gt would be handed
    text and raise. The node sees a double, and so should the validators. Plain
    bool words such as 'y' are converted for the same reason, while a quoted
    scalar stays text because that is what the node sees.
    """
    scalar = parameter.scalar_type
    if scalar in ('int', 'double'):
        convert = (lambda text: int(text, 10)) if scalar == 'int' else float
        if reads_as_number(value, scalar):
            return convert(value)
        if isinstance(value, list):
            return [
                convert(item) if reads_as_number(item, scalar) else item
                for item in value
            ]
    if scalar == 'bool':
        if reads_as_bool(value):
            return value.lower() in RCL_TRUE_WORDS
        if isinstance(value, list):
            return [
                item.lower() in RCL_TRUE_WORDS if reads_as_bool(item) else item
                for item in value
            ]
    return value


def runtime_default(parameter: 'DeclaredParameter') -> Any:
    """Return the default_value the way the generated code holds it.

    A default is compiled into the node as a literal, not parsed by
    rcl_yaml_param_parser, and the generator converts an integer written for a
    double, so `default_value: 1` is the double 1.0 at runtime.
    """
    value = parameter.default_value
    if parameter.scalar_type != 'double':
        return value

    def as_double(item):
        is_int = isinstance(item, int) and not isinstance(item, bool)
        return float(item) if is_int else item

    if isinstance(value, list):
        return [as_double(item) for item in value]
    return as_double(value)


def check_type(parameter: DeclaredParameter, value: Any) -> Optional[str]:
    """Return an error message when a configured value does not match the declared type."""
    scalar = parameter.scalar_type
    size = parameter.fixed_size

    if not parameter.is_array:
        problem = check_scalar_type(scalar, value)
        if problem is not None:
            return problem
        if scalar == 'string' and reads_as_bool(value):
            return (
                f'ROS 2 reads {value} as a bool unless it is quoted, and this '
                f'parameter is declared as a string'
            )
        if size is not None and scalar == 'string' and len(value) > size:
            return f'string is longer than the fixed size of {size}'
        return None

    if not isinstance(value, list):
        return f"expected type '{scalar}_array', got '{yaml_type_name(value)}'"
    if not value:
        return (
            'an empty sequence gives the node no value at all; ROS 2 reads it '
            'as PARAMETER_NOT_SET rather than as an empty array'
        )
    if size is not None and len(value) > size:
        return f'array has {len(value)} elements, more than the fixed size of {size}'
    for index, element in enumerate(value):
        problem = check_scalar_type(scalar, element)
        if problem is not None:
            return f'element {index} of the array: {problem}'
        if scalar == 'string' and reads_as_bool(element):
            return (
                f'element {index} of the array: ROS 2 reads {element} as a bool '
                f'unless it is quoted, and this parameter is declared as a '
                f'string_array'
            )
    return None


def run_validations(parameter: DeclaredParameter, value: Any) -> List[Tuple[str, str]]:
    """Replay the definition's validators and return (severity, message) pairs.

    A validator that rejects the value is an error. A validator that cannot run
    here, because it is written in C++ or because it raised, is a warning: the
    value may well be correct and only the check is missing.
    """
    results = []
    for validation in parameter.validations:
        name = validation.function_base_name
        function = getattr(ParameterValidators, name, None)
        if function is None:
            results.append(
                (
                    WARNING,
                    f'custom validator {validation.function_name} is C++ and '
                    f'cannot be evaluated here, not checked',
                )
            )
            continue
        try:
            result = function(
                _ValidatorParam(parameter.name, value), *validation.arguments
            )
        except Exception as error:  # noqa: BLE001 - a validator must not stop the run
            results.append(
                (
                    WARNING,
                    f'validator {name} raised {type(error).__name__}: {error}, '
                    f'not checked',
                )
            )
            continue
        if result:
            results.append((ERROR, result))
    return results


def node_name_of(section: str) -> str:
    """Reduce a configuration section name to the node name it refers to.

    A section may be written with a leading slash or under a namespace, while a
    definition's root element is always the bare node name.
    """
    return section.strip('/').rsplit('/', 1)[-1]


def join_name(prefix: str, part: Any) -> str:
    """Join a dotted parameter name, tolerating an empty prefix."""
    return f'{prefix}.{part}' if prefix else str(part)


def flatten(tree: Dict, prefix: str = '') -> Dict[str, Any]:
    """Flatten a nested mapping into dotted names."""
    flat = {}
    for key, value in tree.items():
        name = join_name(prefix, key)
        if isinstance(value, dict):
            flat.update(flatten(value, name))
        else:
            flat[name] = value
    return flat


def expand_mapped_name(
    name: str,
    mapped_params: List[str],
    values: Dict[str, Any],
    declared: Dict[str, 'DeclaredParameter'],
) -> Optional[List[str]]:
    """Resolve the __map_ segments of a name using the keys found in the config.

    Returns None when a map's key list is missing from the configuration, since
    the set of parameters to expect cannot be known in that case.
    """
    names = ['']
    index = 0
    for segment in name.split('.'):
        if segment.startswith('__map_'):
            if index >= len(mapped_params):
                return None
            key_name = mapped_params[index]
            index += 1
            keys = values.get(key_name)
            if keys is None and key_name in declared:
                # The node expands the map over the effective value, which is
                # the declared default when the configuration sets nothing.
                keys = declared[key_name].default_value
            if not isinstance(keys, list):
                return None
            names = [join_name(base, key) for base in names for key in keys]
        else:
            names = [join_name(base, segment) for base in names]
    return names


def load_definition(path: str):
    """Parse a parameter definition file and return the generator holding it."""
    generator = GenerateCode('markdown')
    generator.parse(path, '')
    return generator


def definition_namespace(path: str) -> Optional[str]:
    """Read the root element of a definition without parsing its parameters.

    Raises ConfigError when the file does not have exactly one root element.
    """
    document = load_yaml(path)
    keys = list(document)
    if len(keys) != 1:
        raise ConfigError(
            f'{path}: a parameter definition must have exactly one root '
            f'element, found {len(keys)}'
        )
    return keys[0]


def load_definitions(
    paths: List[str], used: Set[str]
) -> Tuple[Dict[str, Any], List[str], List[str]]:
    """Parse the definitions whose namespace a configuration actually uses.

    Parsing a definition runs the same per parameter work as code generation, so
    with many definitions on the command line only the ones a configuration
    refers to are parsed. A single definition is always parsed, because it is
    applied to every section. Returns the parsed definitions and the paths that
    were left out, which the caller reports so that skipping stays visible.
    """
    if len(paths) == 1:
        generator = read_definition(paths[0])
        return {generator.namespace: generator}, [], []
    generators = {}
    sources = {}
    unused = []
    duplicates = []
    for path in paths:
        namespace = definition_namespace(path)
        if namespace in used:
            generator = read_definition(path)
            if generator.namespace in generators:
                duplicates.append(
                    f'{generator.namespace} is declared by both '
                    f'{sources[generator.namespace]} and {path}'
                )
                continue
            generators[generator.namespace] = generator
            sources[generator.namespace] = path
        else:
            unused.append(path)
    return generators, unused, duplicates


def declared_parameters(
    generator, values: Dict[str, Any]
) -> Tuple[Dict[str, DeclaredParameter], List[str]]:
    """Flatten a definition into dotted names, expanding mapped parameters.

    Parameters of type none are left out. The generator declares nothing for
    them, so the node neither requires them nor gives them a type; their names
    are returned separately so that the strict check can leave their subtree
    alone.
    """
    parameters = {}
    free_form = []
    for declaration in generator.declare_parameters:
        parameter = DeclaredParameter(declaration)
        if parameter.scalar_type == 'none':
            free_form.append(parameter.name)
            continue
        parameters[parameter.name] = parameter
    for declaration in generator.declare_dynamic_parameters:
        template = DeclaredParameter(declaration)
        if template.scalar_type == 'none':
            free_form.append(template.name)
            continue
        names = expand_mapped_name(
            template.name, declaration.mapped_params, values, parameters
        )
        if names is None:
            continue
        for name in names:
            parameters[name] = DeclaredParameter(declaration, name=name)
    return parameters, free_form


def join_node_name(namespace: str, key: str) -> str:
    """Append a key to a node name the way rcl_yaml_param_parser does.

    The levels are joined with a slash unless the name already ends with one,
    so `/ns: {ctrl: ...}` and `/ns/: {ctrl: ...}` both name `/ns/ctrl`.
    """
    if not namespace:
        return key
    return namespace + key if namespace.endswith('/') else f'{namespace}/{key}'


def node_sections(document: Dict) -> Dict[str, Dict[str, Any]]:
    """Return the parameter tree of every node in a ROS parameter file.

    A `ros__parameters` key may sit under any number of namespace levels, as
    in `robot: {arm: {my_node: {ros__parameters: ...}}}`, so the mapping is
    walked recursively and the levels are joined into the section name. The
    sections keep the order of the file, which decides precedence. A file
    without any `ros__parameters` key is treated as a single unnamed section,
    so that plain parameter trees can be validated too.

    Raises ConfigError for a name rcl_yaml_param_parser rejects, which makes
    the whole file fail to load.
    """

    def walk(tree: Dict[str, Any], namespace: str) -> None:
        for key, value in tree.items():
            if not isinstance(value, dict):
                continue
            name = join_node_name(namespace, str(key))
            if ROS_PARAMETERS_KEY in value:
                if '//' in name:
                    raise ConfigError(
                        f'{name} contains a repeated forward slash, '
                        f'rcl_yaml_param_parser rejects the whole file'
                    )
                sections[name] = value[ROS_PARAMETERS_KEY] or {}
                continue
            walk(value, name)

    sections: Dict[str, Dict[str, Any]] = {}
    walk(document, '')
    if not sections:
        return {'': document}
    return sections


def fully_qualified(section: str) -> str:
    return section if section.startswith('/') else f'/{section}'


def is_wildcard_node(section: str) -> bool:
    return node_name_of(section) in WILDCARD_NAMES


def section_matches(section: str, node_fqn: str) -> bool:
    """Does a section apply to the node, as rclcpp's is_node_name_matched decides?

    `/*` stands for exactly one level and `/**` for any number of levels.
    """
    pattern = fully_qualified(section).replace('/*', r'(/\w+)')
    try:
        return re.fullmatch(pattern, node_fqn) is not None
    except re.error:
        return False


def stand_in_node(section: str) -> str:
    """A node name that a wildcard section describes, to match others against."""
    return '/'.join(
        WILDCARD_STAND_IN if level in WILDCARD_NAMES else level
        for level in fully_qualified(section).split('/')
    )


def effective_sections(
    sections: Dict[str, Dict[str, Any]],
) -> List[Tuple[str, Dict[str, Any]]]:
    """Return the values each node described by a file receives at runtime.

    rclcpp applies every section whose name matches the node, wildcard or not,
    in file order, so a later section wins over an earlier one. A section whose
    node name is a wildcard describes no node of its own; it is only validated
    when the file has no other section, the usual shape when the node name is
    not pinned. Sections that name the same node, such as `/ns/ctrl` and
    `ns: {ctrl: ...}`, are validated once.
    """
    if '' in sections:
        return [('', flatten(sections['']))]
    names = list(sections)
    nodes = [name for name in names if not is_wildcard_node(name)] or names
    targets: Dict[str, str] = {}
    for name in nodes:
        targets.setdefault(stand_in_node(name), name)
    effective = []
    for node_fqn, name in targets.items():
        values: Dict[str, Any] = {}
        for other in names:
            if section_matches(other, node_fqn):
                values.update(flatten(sections[other]))
        effective.append((name, values))
    return effective


def is_exempt(name: str, free_form: List[str]) -> bool:
    """Is this configuration key one the definition is not expected to declare?

    Every node declares a few parameters for itself, and the subtree under a
    parameter of type none is free form by construction.
    """
    if name in BUILT_IN_PARAMETERS or name.startswith(BUILT_IN_PREFIXES):
        return True
    return any(name == root or name.startswith(f'{root}.') for root in free_form)


def validate_section(
    location: str,
    generator,
    values: Dict[str, Any],
    strict: bool,
) -> List[Diagnostic]:
    """Validate one node's parameters against one definition."""
    diagnostics = []
    parameters, free_form = declared_parameters(generator, values)

    for name, parameter in sorted(parameters.items()):
        where = join_name(location, name)
        if name not in values:
            if not parameter.has_default:
                diagnostics.append(
                    Diagnostic(
                        ERROR,
                        where,
                        'missing from config and the definition sets no '
                        'default_value, the node will fail to start',
                    )
                )
                continue
            # The node validates the effective value, which is the declared
            # default when the configuration sets nothing, so the default has
            # to pass the definition's validators. Its type is not checked:
            # the generator already did that at build time, and the rules in
            # check_type are about how rcl_yaml_param_parser reads text, which
            # does not apply to a compiled-in literal such as [] or 1.
            problem = None
            for severity, message in run_validations(
                parameter, runtime_default(parameter)
            ):
                if severity == ERROR:
                    problem = message
                    break
            if problem is not None:
                diagnostics.append(
                    Diagnostic(
                        ERROR,
                        where,
                        f'not set by the config and the default_value '
                        f'{parameter.default_value} is invalid: {problem}',
                    )
                )
                continue
            if strict:
                diagnostics.append(
                    Diagnostic(
                        WARNING,
                        where,
                        f'missing from config, will use default_value '
                        f'{parameter.default_value}',
                    )
                )
            continue

        value = values[name]
        problem = check_type(parameter, value)
        if problem is not None:
            diagnostics.append(Diagnostic(ERROR, where, problem))
            continue
        value = coerce_value(parameter, value)
        for severity, message in run_validations(parameter, value):
            diagnostics.append(Diagnostic(severity, where, message))

    if strict:
        unknown = [
            name
            for name in sorted(values)
            if name not in parameters and not is_exempt(name, free_form)
        ]
        # Every suggestion compares the name against every declared parameter, so
        # they are only worth computing while there are few names to suggest for.
        # A configuration that has drifted wholesale is not helped by a list of
        # guesses anyway.
        suggest = len(unknown) <= MAX_SUGGESTIONS
        for name in unknown:
            where = join_name(location, name)
            close = (
                difflib.get_close_matches(name, parameters.keys(), n=1)
                if suggest
                else []
            )
            hint = f" (did you mean '{close[0]}'?)" if close else ''
            diagnostics.append(Diagnostic(ERROR, where, f'unknown parameter{hint}'))

    return diagnostics


class ConfigError(Exception):
    """A file could not be read or parsed, reported without a traceback."""


def load_yaml(path: str) -> Dict:
    try:
        with open(path) as handle:
            # The custom loader remembers which scalars were quoted, which is
            # what decides the type ROS 2 gives them at runtime.
            document = yaml.load(handle, Loader=ConfigLoader)
    except OSError as error:
        raise ConfigError(f'{path}: {error.strerror or error}')
    except yaml.YAMLError as error:
        raise ConfigError(f'{path}: {error}')
    if document is None:
        return {}
    if not isinstance(document, dict):
        raise ConfigError(f'{path}: the document is not a mapping')
    return document


def read_config(path: str) -> Dict[str, Dict[str, Any]]:
    """Load a configuration file and split it into its node sections."""
    document = load_yaml(path)
    try:
        return node_sections(document)
    except ConfigError as error:
        raise ConfigError(f'{path}: {error}')


def read_definition(path: str):
    """Parse a definition, reporting a bad file without a traceback."""
    try:
        return load_definition(path)
    except ConfigError:
        raise
    except Exception as error:  # noqa: BLE001 - the parser raises several types
        raise ConfigError(f'{path}: {error}')


def validate(
    definition_paths: List[str],
    config_paths: List[str],
    strict: bool = False,
) -> List[Diagnostic]:
    """Validate every config against the definitions whose namespace matches."""
    diagnostics = []
    configs = [(path, read_config(path)) for path in config_paths]
    used = {node_name_of(name) for _, sections in configs for name in sections}
    definitions, unused, duplicates = load_definitions(definition_paths, used)
    single_definition = len(definition_paths) == 1

    for message in duplicates:
        diagnostics.append(Diagnostic(ERROR, 'parameter definitions', message))
    if unused:
        shown = ', '.join(os.path.basename(path) for path in unused[:5])
        if len(unused) > 5:
            shown += f' and {len(unused) - 5} more'
        diagnostics.append(
            Diagnostic(
                WARNING,
                'parameter definitions',
                f'{len(unused)} matched no configuration section and were not '
                f'checked: {shown}',
            )
        )

    for config_path, sections in configs:
        nodes = effective_sections(sections)
        matched = any(node_name_of(name) in definitions for name, _ in nodes)
        for section_name, values in nodes:
            node_name = node_name_of(section_name)
            if node_name in definitions:
                generator = definitions[node_name]
            elif single_definition and not matched:
                generator = next(iter(definitions.values()))
            else:
                diagnostics.append(
                    Diagnostic(
                        WARNING,
                        f'{config_path}:{section_name}',
                        'no parameter definition has this namespace, not checked',
                    )
                )
                continue
            diagnostics.extend(
                validate_section(section_name, generator, values, strict)
            )
    return diagnostics


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog='generate_parameter_library_validate',
        description='Validate ROS 2 parameter configuration files against '
        'generate_parameter_library parameter definitions, without a ROS 2 '
        'installation or a built workspace.',
    )
    parser.add_argument(
        '--param-definition',
        action='append',
        required=True,
        metavar='FILE',
        help='a parameter definition YAML, may be given more than once',
    )
    parser.add_argument(
        '--config',
        action='append',
        required=True,
        metavar='FILE',
        help='a parameter configuration YAML to validate, may be given more '
        'than once',
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='also report parameters that no definition declares and '
        'parameters missing from the config that will take their default',
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        diagnostics = validate(args.param_definition, args.config, args.strict)
    except ConfigError as error:
        print(f'{ERROR}: {error}', file=sys.stderr)
        return 1
    # One stream keeps errors and warnings in the order they were found.
    for diagnostic in diagnostics:
        print(diagnostic, file=sys.stderr)
    errors = sum(1 for d in diagnostics if d.severity == ERROR)
    if errors:
        print(f'{errors} error(s) found', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
