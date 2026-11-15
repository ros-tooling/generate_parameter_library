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

"""Messages of the element bound validators name the offending element and bound."""

from types import SimpleNamespace

from generate_parameter_library_py.python_validators import ParameterValidators


def param(value):
    return SimpleNamespace(name='gains', value=value)


def test_upper_element_bounds_names_the_upper_bound():
    assert ParameterValidators.upper_element_bounds(param([1.0, 12.0]), 10.0) == (
        "Value 12.0 in parameter 'gains' must be below upper bound of 10.0"
    )


def test_lower_element_bounds_names_the_lower_bound():
    assert ParameterValidators.lower_element_bounds(param([1.0, -2.0]), 0.0) == (
        "Value -2.0 in parameter 'gains' must be above lower bound of 0.0"
    )


def test_element_bounds_names_the_element():
    assert ParameterValidators.element_bounds(param([1.0, 12.0]), 0.0, 10.0) == (
        "Value 12.0 in parameter 'gains' must be within bounds [0.0, 10.0]"
    )


def test_elements_within_bounds_pass():
    assert ParameterValidators.element_bounds(param([0.0, 10.0]), 0.0, 10.0) == ''
    assert ParameterValidators.upper_element_bounds(param([10.0]), 10.0) == ''
