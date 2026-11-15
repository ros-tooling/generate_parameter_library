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

"""refresh_dynamic_parameters() of a generated Python module, run on a real node."""

import importlib.util

import pytest

from generate_parameter_library_py.generate_python_module import run

rclpy = pytest.importorskip('rclpy')
from rclpy.parameter import Parameter  # noqa: E402

# pid is the only map keyed by joints.
DEFINITION = """
ctrl:
  joints:
    type: string_array
    default_value: ["a", "b"]
  pid:
    rate:
      type: double
      default_value: 1.0
    __map_joints:
      p:
        type: double
        default_value: 1.0
      i:
        type: double
        default_value: 0.5
"""

# The key array and one key are named like the map helpers once were.
NAMES_DEFINITION = DEFINITION.replace('joints', 'entry_names').replace(
    '"b"', '"entry_names"'
)


@pytest.fixture
def listener_and_node(tmp_path, request):
    definition = tmp_path / 'parameters.yaml'
    definition.write_text(getattr(request, 'param', DEFINITION))
    output = tmp_path / 'ctrl_parameters.py'
    run(str(output), str(definition), '', False)
    spec = importlib.util.spec_from_file_location('ctrl_parameters', output)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    rclpy.init()
    node = rclpy.create_node('ctrl')
    try:
        yield module.ctrl.ParamListener(node), node
    finally:
        node.destroy_node()
        rclpy.shutdown()


@pytest.mark.parametrize('listener_and_node', [NAMES_DEFINITION], indirect=True)
def test_names_of_former_map_helpers_are_plain_names(listener_and_node):
    listener, node = listener_and_node
    assert listener.get_params().pid.get_entry('entry_names').p == 1.0

    node.set_parameters([Parameter('entry_names', value=['a'])])
    listener.refresh_dynamic_parameters()

    with pytest.raises(AttributeError):
        listener.get_params().pid.get_entry('entry_names')


def test_values_kept_on_the_node_are_restored(listener_and_node):
    listener, node = listener_and_node
    node.set_parameters([Parameter('pid.a.i', value=8.0)])
    node.set_parameters([Parameter('joints', value=['b'])])
    listener.refresh_dynamic_parameters()

    # setting p recreates the entry in update(), with the default i
    node.set_parameters([Parameter('joints', value=['a', 'b'])])
    node.set_parameters([Parameter('pid.a.p', value=5.0)])
    listener.refresh_dynamic_parameters()

    entry = listener.get_params().pid.get_entry('a')
    assert (entry.p, entry.i) == (5.0, 8.0)


def test_refresh_does_not_revert_an_update_made_meanwhile(listener_and_node):
    listener, node = listener_and_node
    node.set_parameters([Parameter('joints', value=['a'])])
    get_parameter = node.get_parameter
    reads = []

    def get_parameter_while_another_thread_sets_rate(name):
        reads.append(name)
        # the second read of pid.a.p is the first one after refresh's snapshot
        if reads.count('pid.a.p') == 2:
            node.set_parameters([Parameter('pid.rate', value=3.0)])
        return get_parameter(name)

    node.get_parameter = get_parameter_while_another_thread_sets_rate
    listener.refresh_dynamic_parameters()

    params = listener.get_params()
    assert params.pid.rate == 3.0
    with pytest.raises(AttributeError):
        params.pid.get_entry('b')


def test_refresh_without_changes_keeps_the_stamp(listener_and_node):
    listener, _ = listener_and_node
    before = listener.get_params()
    listener.refresh_dynamic_parameters()
    assert not listener.is_old(before)
