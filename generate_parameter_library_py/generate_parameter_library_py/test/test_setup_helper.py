# Copyright 2026 Marq Rasmussen
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
#    * Neither the name of the copyright holder nor the names of its
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
import subprocess
import sys
import tarfile
import types

import pytest

import generate_parameter_library_py
from generate_parameter_library_py.setup_helper import (
    _resolve_package,
    parameter_cmdclass,
)

LIBRARY_PATH = os.path.dirname(os.path.dirname(generate_parameter_library_py.__file__))

PARAMETERS_YAML = """probe:
  frame:
    type: string
    default_value: probe_frame
    description: The frame
"""

SETUP_PY = """from setuptools import setup

from generate_parameter_library_py.setup_helper import parameter_cmdclass

setup(
    name='probe',
    version='0.0.0',
    packages=['probe'],
    {package_dir}
    cmdclass=parameter_cmdclass('probe_parameters', '{yaml_file}'{package_arg}),
)
"""


def write_package(root, yaml_file, init_content=None, package_dir='', package_arg=''):
    """Write a throwaway `probe` distribution under root and return root."""
    package_path = os.path.join(root, package_dir, 'probe')
    os.makedirs(package_path, exist_ok=True)
    if init_content is not None:
        with open(os.path.join(package_path, '__init__.py'), 'w') as f:
            f.write(init_content)
    yaml_path = os.path.join(root, yaml_file)
    os.makedirs(os.path.dirname(yaml_path), exist_ok=True)
    with open(yaml_path, 'w') as f:
        f.write(PARAMETERS_YAML)
    with open(os.path.join(root, 'setup.py'), 'w') as f:
        f.write(
            SETUP_PY.format(
                yaml_file=yaml_file,
                package_dir=(
                    f"package_dir={{'': '{package_dir}'}}," if package_dir else ''
                ),
                package_arg=package_arg,
            )
        )
    return root


def run_setup(cwd, *args):
    env = dict(os.environ)
    env['PYTHONPATH'] = os.pathsep.join(
        [LIBRARY_PATH] + [p for p in [env.get('PYTHONPATH')] if p]
    )
    result = subprocess.run(
        [sys.executable, 'setup.py', *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def build(root, tmp_path):
    """Run `setup.py build` the way colcon does and return build_lib."""
    build_base = os.path.join(tmp_path, 'build', 'probe', 'build')
    run_setup(root, 'build', '--build-base', build_base)
    return os.path.join(build_base, 'lib')


def default_frame(path, module='probe.probe_parameters', name='probe'):
    """Import module from path and return the frame default of its `name` struct."""
    code = (
        'import importlib, sys; sys.path.insert(0, sys.argv[1]); '
        'm = importlib.import_module(sys.argv[2]); '
        'print(getattr(m, sys.argv[3]).Params().frame)'
    )
    result = subprocess.run(
        [sys.executable, '-c', code, path, module, name],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def read(path):
    with open(path) as f:
        return f.read()


def test_build_keeps_user_init(tmp_path):
    root = write_package(
        str(tmp_path / 'src'), 'probe/parameters.yaml', init_content='VALUE = 1\n'
    )
    build_lib = build(root, str(tmp_path))

    assert default_frame(build_lib) == 'probe_frame'
    assert read(os.path.join(build_lib, 'probe', '__init__.py')) == 'VALUE = 1\n'
    # Nothing is pre-written into an install tree, where it would shadow the
    # package's own __init__.py at install time.
    assert not os.path.exists(tmp_path / 'install')


def test_build_adds_init_when_source_has_none(tmp_path):
    root = write_package(str(tmp_path / 'src'), 'probe/parameters.yaml')
    build_lib = build(root, str(tmp_path))

    assert read(os.path.join(build_lib, 'probe', '__init__.py')) == ''
    assert default_frame(build_lib) == 'probe_frame'


def test_build_src_layout(tmp_path):
    root = write_package(
        str(tmp_path / 'src'),
        'src/probe/parameters.yaml',
        init_content='VALUE = 2\n',
        package_dir='src',
    )
    build_lib = build(root, str(tmp_path))

    assert os.path.isfile(os.path.join(build_lib, 'probe', 'probe_parameters.py'))
    assert default_frame(build_lib) == 'probe_frame'
    assert read(os.path.join(build_lib, 'probe', '__init__.py')) == 'VALUE = 2\n'


def test_sdist_rebuilds_from_unpacked_archive(tmp_path):
    root = write_package(
        str(tmp_path / 'src'), 'probe/parameters.yaml', init_content=''
    )
    dist_dir = str(tmp_path / 'dist')
    run_setup(root, 'sdist', '--dist-dir', dist_dir, '--formats', 'gztar')
    unpacked = tmp_path / 'unpacked'
    with tarfile.open(os.path.join(dist_dir, 'probe-0.0.0.tar.gz')) as archive:
        archive.extractall(unpacked)
    build_lib = build(str(unpacked / 'probe-0.0.0'), str(tmp_path / 'rebuild'))

    assert default_frame(build_lib) == 'probe_frame'


def test_develop_through_symlink_resolves_yaml_against_source(tmp_path):
    # colcon runs `setup.py develop` from build/<pkg>, where setup.py and the
    # package directory are symlinks into the source tree.
    source = write_package(
        str(tmp_path / 'src'),
        'config/parameters.yaml',
        init_content='VALUE = 1\n',
        package_arg=", package='probe'",
    )
    build_dir = tmp_path / 'build' / 'probe'
    build_dir.mkdir(parents=True)
    os.symlink(os.path.join(source, 'setup.py'), build_dir / 'setup.py')
    os.symlink(os.path.join(source, 'probe'), build_dir / 'probe')
    run_setup(
        str(build_dir), 'develop', '--prefix', str(tmp_path / 'prefix'), '--no-deps'
    )

    assert os.path.isfile(os.path.join(source, 'probe', 'probe_parameters.py'))
    assert default_frame(source) == 'probe_frame'


def test_develop_generates_into_source_without_init(tmp_path):
    root = write_package(str(tmp_path / 'src'), 'probe/parameters.yaml')
    run_setup(root, 'develop', '--prefix', str(tmp_path / 'prefix'), '--no-deps')

    assert sorted(os.listdir(os.path.join(root, 'probe'))) == [
        'parameters.yaml',
        'probe_parameters.py',
    ]
    assert default_frame(root) == 'probe_frame'


MULTI_MODULE_SETUP_PY = """from setuptools import setup

from generate_parameter_library_py.setup_helper import parameter_cmdclass

setup(
    name='probe',
    version='0.0.0',
    packages=['probe', 'probe_extra'],
    cmdclass=parameter_cmdclass(
        modules=[
            {'module_name': 'probe_parameters', 'yaml_file': 'probe/parameters.yaml'},
            {
                'module_name': 'extra_parameters',
                'yaml_file': 'config/extra.yaml',
                'package': 'probe_extra',
            },
        ]
    ),
)
"""


def write_multi_module_package(root):
    write_package(root, 'probe/parameters.yaml')
    os.makedirs(os.path.join(root, 'probe_extra'))
    os.makedirs(os.path.join(root, 'config'))
    with open(os.path.join(root, 'config', 'extra.yaml'), 'w') as f:
        f.write(PARAMETERS_YAML.replace('probe', 'extra'))
    with open(os.path.join(root, 'setup.py'), 'w') as f:
        f.write(MULTI_MODULE_SETUP_PY)
    return root


def test_build_multiple_modules(tmp_path):
    root = write_multi_module_package(str(tmp_path / 'src'))
    build_lib = build(root, str(tmp_path))

    assert default_frame(build_lib) == 'probe_frame'
    assert (
        default_frame(build_lib, 'probe_extra.extra_parameters', 'extra')
        == 'extra_frame'
    )


def test_develop_multiple_modules(tmp_path):
    root = write_multi_module_package(str(tmp_path / 'src'))
    run_setup(root, 'develop', '--prefix', str(tmp_path / 'prefix'), '--no-deps')

    assert default_frame(root) == 'probe_frame'
    assert default_frame(root, 'probe_extra.extra_parameters', 'extra') == 'extra_frame'


def pip_available():
    result = subprocess.run(
        [sys.executable, '-m', 'pip', '--version'], capture_output=True
    )
    return result.returncode == 0


def setuptools_supports_pep660():
    # PEP 660 editable wheels need setuptools' build_editable hook, added in 64.
    import setuptools
    from packaging.version import Version

    return Version(setuptools.__version__) >= Version('64')


def pip_supports_break_system_packages():
    # --break-system-packages bypasses PEP 668; pip added it in 23.1, alongside
    # PEP 668 support itself, so older pip neither needs nor accepts it.
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '--help'], capture_output=True
    )
    return b'--break-system-packages' in result.stdout


@pytest.mark.skipif(not pip_available(), reason='pip is not installed')
@pytest.mark.skipif(
    not setuptools_supports_pep660(),
    reason='setuptools < 64 has no PEP 660 editable support',
)
def test_pip_editable_generates_into_source(tmp_path):
    # PEP 660 editable wheels run build_py in editable mode; the source tree is
    # what gets imported.
    root = write_package(
        str(tmp_path / 'src'), 'probe/parameters.yaml', init_content='VALUE = 1\n'
    )
    env = dict(os.environ)
    env['PYTHONPATH'] = os.pathsep.join(
        [LIBRARY_PATH] + [p for p in [env.get('PYTHONPATH')] if p]
    )
    pip_args = [
        sys.executable,
        '-m',
        'pip',
        'install',
        '--editable',
        '.',
        '--use-pep517',
        '--no-build-isolation',
        '--no-deps',
        '--no-index',
        '--prefix',
        str(tmp_path / 'prefix'),
    ]
    if pip_supports_break_system_packages():
        pip_args.insert(-2, '--break-system-packages')
    result = subprocess.run(
        pip_args,
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    assert default_frame(root) == 'probe_frame'
    assert read(os.path.join(root, 'probe', '__init__.py')) == 'VALUE = 1\n'


LEGACY_SETUP_PY = """import sys

from setuptools import setup

if len(sys.argv) >= 2 and sys.argv[1] != 'clean':
    from generate_parameter_library_py.setup_helper import generate_parameter_module

    generate_parameter_module('probe_parameters', 'probe/parameters.yaml')

setup(name='probe', version='0.0.0', packages=['probe'])
"""


def test_legacy_generate_parameter_module_still_generates(tmp_path):
    root = write_package(str(tmp_path / 'src'), 'probe/parameters.yaml')
    with open(os.path.join(root, 'setup.py'), 'w') as f:
        f.write(LEGACY_SETUP_PY)
    build(root, str(tmp_path))

    # The legacy helper writes next to the colcon build base.
    assert default_frame(str(tmp_path / 'build' / 'probe')) == 'probe_frame'


def test_modules_rejects_top_level_arguments():
    with pytest.raises(ValueError, match='or modules'):
        parameter_cmdclass(
            package='probe',
            modules=[{'module_name': 'm', 'yaml_file': 'probe/parameters.yaml'}],
        )


def test_resolve_package_requires_explicit_package():
    distribution = types.SimpleNamespace(packages=['other'], get_name=lambda: 'dist')

    with pytest.raises(ValueError, match='config/parameters.yaml; pass package='):
        _resolve_package(distribution, None, 'config/parameters.yaml')
