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
        listener = module.ctrl.ParamListener(node)
        listener.module = module
        yield listener, node
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


def run_once_when_the_sync_starts(listener, monkeypatch, action):
    """Run action, as another thread would, between refresh's snapshot and store."""
    entry_names = listener.module._map_entry_names
    ran = []

    def entry_names_after_action(struct):
        # the declare step does not list entries, the sync starts with it
        if not ran:
            ran.append(True)
            action()
        return entry_names(struct)

    monkeypatch.setattr(listener.module, '_map_entry_names', entry_names_after_action)


def test_refresh_does_not_revert_an_update_made_meanwhile(
    listener_and_node, monkeypatch
):
    listener, node = listener_and_node
    node.set_parameters([Parameter('joints', value=['a'])])
    run_once_when_the_sync_starts(
        listener,
        monkeypatch,
        lambda: node.set_parameters([Parameter('pid.rate', value=3.0)]),
    )
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


def test_key_added_while_refreshing_is_declared_before_it_is_read(
    listener_and_node, monkeypatch
):
    listener, node = listener_and_node
    run_once_when_the_sync_starts(
        listener,
        monkeypatch,
        lambda: node.set_parameters([Parameter('joints', value=['a', 'b', 'c'])]),
    )
    listener.refresh_dynamic_parameters()

    assert node.has_parameter('pid.c.p')
    assert listener.get_params().pid.get_entry('c').p == 1.0


def test_get_params_keeps_the_stamp_of_an_update_made_meanwhile(
    listener_and_node, monkeypatch
):
    listener, node = listener_and_node
    before = listener.get_params()
    copy_module = listener.module.copy
    deepcopy = copy_module.deepcopy
    updated = []

    def deepcopy_while_another_thread_updates(*args, **kwargs):
        if not updated:
            updated.append(True)
            node.set_parameters([Parameter('pid.rate', value=3.0)])
        return deepcopy(*args, **kwargs)

    monkeypatch.setattr(copy_module, 'deepcopy', deepcopy_while_another_thread_updates)
    listener.get_params()
    monkeypatch.undo()

    assert listener.is_old(before)
    assert listener.get_params().pid.rate == 3.0


def test_refresh_keeps_a_value_the_node_has_not_committed_yet(listener_and_node):
    """update() runs in the on-set callback, before the node stores the value."""
    listener, node = listener_and_node
    # what a setter on another thread has done when refresh runs in between
    listener.update([Parameter('pid.a.p', value=5.0)])
    listener.refresh_dynamic_parameters()

    assert listener.get_params().pid.get_entry('a').p == 5.0
