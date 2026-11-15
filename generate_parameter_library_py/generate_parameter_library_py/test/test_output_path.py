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

"""The generators accept an output file name without a directory."""

import pytest

from generate_parameter_library_py.generate_cpp_header import run as run_cpp
from generate_parameter_library_py.generate_markdown import run as run_markdown
from generate_parameter_library_py.generate_python_module import run as run_python


@pytest.fixture
def definition(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / 'parameters.yaml'
    path.write_text('bare:\n  rate:\n    type: double\n    default_value: 1.0\n')
    return str(path)


def test_cpp_header_in_current_directory(definition, tmp_path):
    run_cpp('bare.hpp', definition, '')
    assert 'namespace bare' in (tmp_path / 'bare.hpp').read_text()


def test_python_module_in_current_directory(definition, tmp_path):
    run_python('bare.py', definition, '')
    assert 'class bare' in (tmp_path / 'bare.py').read_text()


def test_markdown_in_current_directory(definition, tmp_path):
    run_markdown(definition, 'bare.md', 'markdown')
    assert 'rate' in (tmp_path / 'bare.md').read_text()
