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


# TODO: ParameterValidators should be moved somewhere else, like rsl for C++
class ParameterValidators:
    # Value validators

    def lt(param, value):
        if not param.value < value:
            tmp = 'less than'
            return f"Parameter '{param.name}' with the value {param.value} must be {tmp} {value}"
        return ''

    def gt(param, value):
        if not param.value > value:
            tmp = 'greater than'
            return f"Parameter '{param.name}' with the value {param.value} must be {tmp} {value}"
        return ''

    def lt_eq(param, value):
        if not param.value <= value:
            tmp = 'below upper bound of'
            return f"Parameter '{param.name}' with the value {param.value} must be {tmp} {value}"
        return ''

    def gt_eq(param, value):
        if not param.value >= value:
            tmp = 'above lower bound of'
            return f"Parameter '{param.name}' with the value {param.value} must be {tmp} {value}"
        return ''

    def not_empty(param):
        if len(param.value) == 0:
            tmp = 'above lower bound of'
            return f"Parameter '{param.name}' cannot be empty"
        return ''

    def one_of(param, values):
        if not param.value in values:
            return f"Parameter '{param.name}' with the value '{param.value}' is not in the set {str(values)}"
        return ''

    # Array validators
    def unique(param):
        if len(set(param.value)) != len(param.value):
            return f"Parameter '{param.name}' must only contain unique values"
        return ''

    def subset_of(param, values):
        for val in param.value:
            if not val in values:
                return f"Entry '{val}' in parameter '{param.name}' is not in the set {str(values)}"
        return ''

    def fixed_size(param, length):
        if not len(param.value) == length:
            tmp = 'equal to'
            return f"Length of parameter '{param.name}' is '{len(param.value)}' but must be {tmp} {length}"
        return ''

    def size_gt(param, length):
        if not len(param.value) > length:
            tmp = 'greater than'
            return f"Length of parameter '{param.name}' is '{len(param.value)}' but must be {tmp} {length}"
        return ''

    def size_lt(param, length):
        if not len(param.value) < length:
            tmp = 'less than'
            return f"Length of parameter '{param.name}' is '{len(param.value)}' but must be {tmp} {length}"
        return ''

    def element_bounds(param, lower, upper):
        for val in param.value:
            if val > upper or val < lower:
                return f"Value {val} in parameter '{param.name}' must be within bounds [{lower}, {upper}]"
        return ''

    def lower_element_bounds(param, lower):
        for val in param.value:
            if val < lower:
                return f"Value {val} in parameter '{param.name}' must be above lower bound of {lower}"
        return ''

    def upper_element_bounds(param, upper):
        for val in param.value:
            if val > upper:
                return f"Value {val} in parameter '{param.name}' must be below upper bound of {upper}"
        return ''

    def bounds(param, lower, upper):
        if param.value > upper or param.value < lower:
            return f"Value {param.value} in parameter '{param.name}' must be within bounds [{lower}, {upper}]"
        return ''
