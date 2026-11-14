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

from typing import List, Union
from typeguard import typechecked


class PythonConversions:
    def __init__(self):
        self.defined_type_to_lang_type = {
            'none': lambda defined_type, templates: None,
            'bool': lambda defined_type, templates: 'bool',
            'double': lambda defined_type, templates: 'float',
            'int': lambda defined_type, templates: 'int',
            'string': lambda defined_type, templates: 'str',
            'bool_array': lambda defined_type, templates: '[bool]',
            'double_array': lambda defined_type, templates: '[float]',
            'int_array': lambda defined_type, templates: '[int]',
            'string_array': lambda defined_type, templates: '[str]',
            'double_array_fixed': lambda defined_type, templates: '[float]',
            'int_array_fixed': lambda defined_type, templates: '[int]',
            'string_array_fixed': lambda defined_type, templates: '[str]',
            'string_fixed': lambda defined_type, templates: 'str',
        }
        self.yaml_type_to_as_function = {
            'none': None,
            'string_array': 'value',
            'double_array': 'value',
            'int_array': 'value',
            'bool_array': 'value',
            'string': 'value',
            'double': 'value',
            'int': 'value',
            'bool': 'value',
            'double_array_fixed': 'value',
            'int_array_fixed': 'value',
            'string_array_fixed': 'value',
            'string_fixed': 'value',
        }
        self.lang_str_value_func = {
            'none': self.no_code,
            'bool': self.bool_to_str,
            'double': self.float_to_str,
            'int': self.int_to_str,
            'string': self.str_to_str,
            'bool_array': self.bool_array_to_str,
            'double_array': self.float_array_to_str,
            'int_array': self.int_array_to_str,
            'string_array': self.str_array_to_str,
            'double_array_fixed': self.float_array_to_str,
            'int_array_fixed': self.int_array_to_str,
            'string_array_fixed': self.str_array_to_str,
            'string_fixed': self.str_to_str,
        }
        self.python_val_to_str_func = {
            "<class 'bool'>": self.bool_to_str,
            "<class 'float'>": self.float_to_str,
            "<class 'int'>": self.int_to_str,
            "<class 'str'>": self.str_to_str,
        }
        self.python_val_to_yaml_type = {
            "<class 'bool'>": 'bool',
            "<class 'float'>": 'double',
            "<class 'int'>": 'int',
            "<class 'str'>": 'str',
        }
        self.python_list_to_yaml_type = {
            "<class 'bool'>": 'bool_array',
            "<class 'float'>": 'double_array',
            "<class 'int'>": 'integer_array',
            "<class 'str'>": 'string_array',
        }

        self.open_bracket = '['
        self.close_bracket = ']'

    @typechecked
    def get_func_signature(self, function_name: str, base_type: str) -> str:
        if function_name.__contains__('::'):
            # user defined function
            function_name = function_name.replace('::', '.')
        else:
            function_name = 'ParameterValidators.' + function_name
        if function_name.__contains__('<>'):
            function_name = function_name.replace('<>', '')
        return function_name

    @typechecked
    def initialization_fail_validation(self, param_name: str) -> str:
        return f"raise InvalidParameterValueException('{param_name}',param.value, 'Invalid value set during initialization for parameter {param_name}: ' + validation_result)"

    @typechecked
    def initialization_pass_validation(self, param_name: str) -> str:
        return ''

    @typechecked
    def update_parameter_fail_validation(self) -> str:
        return 'return SetParametersResult(successful=False, reason=validation_result)'

    @typechecked
    def update_parameter_pass_validation(self) -> str:
        return ''

    @typechecked
    def no_code(self, s: Union[None, str]):
        return ''

    # value to c++ string conversion functions
    @typechecked
    def bool_to_str(self, cond: Union[None, bool]):
        if cond is None:
            return ''
        return 'True' if cond else 'False'

    @typechecked
    def float_to_str(self, num: Union[None, float]):
        if num is None:
            return ''
        str_num = str(num)
        if str_num == 'nan':
            str_num = "float('nan')"
        elif str_num == 'inf':
            str_num = "float('inf')"
        elif str_num == '-inf':
            str_num = "-float('inf')"
        else:
            if len(str_num.split('.')) == 1 and not str_num.__contains__('e'):
                str_num += '.0'

        return str_num

    @typechecked
    def int_to_str(self, num: Union[None, int]):
        if num is None:
            return ''
        return str(num)

    @typechecked
    def str_to_str(self, s: Union[None, str]):
        if s is None:
            return ''
        return f'"{s}"'

    @typechecked
    def bool_array_to_str(self, values: Union[None, list]):
        if values is None:
            return ''
        return '[' + ', '.join(self.bool_to_str(x) for x in values) + ']'

    @typechecked
    def float_array_to_str(self, values: Union[None, list]):
        if values is None:
            return ''
        return '[' + ', '.join(self.float_to_str(x) for x in values) + ']'

    @typechecked
    def int_array_to_str(self, values: Union[None, list]):
        if values is None:
            return ''
        return '[' + ', '.join(self.int_to_str(x) for x in values) + ']'

    @typechecked
    def str_array_to_str(self, s: Union[None, list]):
        if s is None:
            return ''
        return '[' + ', '.join(self.str_to_str(x) for x in s) + ']'
