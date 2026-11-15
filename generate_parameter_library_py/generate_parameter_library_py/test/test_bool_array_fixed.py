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

from generate_parameter_library_py.generate_cpp_header import run as run_cpp
from generate_parameter_library_py.generate_python_module import run as run_python

DEFINITION = """\
test_params:
  flags:
    type: bool_array_fixed_3
    default_value: [true, false, true]
    description: "fixed-size bool array"
"""


def generate(tmp_path, run, output_name):
    yaml_file = tmp_path / 'params.yaml'
    yaml_file.write_text(DEFINITION)
    output_file = tmp_path / output_name
    run(str(output_file), str(yaml_file))
    return output_file.read_text()


def test_cpp_header_declares_static_bool_vector(tmp_path):
    header = generate(tmp_path, run_cpp, 'params.hpp')

    assert 'rsl::StaticVector<bool, 3> flags = {{true, false, true}};' in header
    assert 'param.as_bool_array()' in header
    assert 'size_lt<bool>(param, 4)' in header


def test_python_module_declares_bool_list(tmp_path):
    module = generate(tmp_path, run_python, 'params.py')

    assert 'self.flags = [True, False, True]' in module
