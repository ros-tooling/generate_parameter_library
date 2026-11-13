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

import sys
import os

from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

from generate_parameter_library_py.generate_python_module import run


def _source_dir(distribution):
    # colcon runs `setup.py develop` from the build directory through a
    # symlinked setup.py; resolve it so paths stay relative to the source.
    return os.path.dirname(os.path.realpath(distribution.script_name or 'setup.py'))


def _resolve_package(distribution, package, yaml_file):
    if package:
        return package
    packages = distribution.packages or []
    candidate = os.path.dirname(os.path.normpath(yaml_file)).replace(os.sep, '.')
    if candidate in packages:
        return candidate
    if distribution.get_name() in packages:
        return distribution.get_name()
    raise ValueError(
        f'Cannot infer the Python package for {yaml_file}; pass package=<name>.'
    )


def _output_file(command, spec, package_root):
    """Return the resolved package of spec and the path its module is written to."""
    module_name, yaml_file, _, package = spec
    package = _resolve_package(command.distribution, package, yaml_file)
    return package, os.path.join(package_root(package), module_name + '.py')


def _generate(command, specs, package_root, add_missing_init):
    """Generate every spec into package_root(package) and return the written files."""
    source_dir = _source_dir(command.distribution)
    outputs = []
    for spec in specs:
        _, yaml_file, validation_module, _ = spec
        package, output_file = _output_file(command, spec, package_root)
        source_init = os.path.join(
            source_dir, command.get_package_dir(package), '__init__.py'
        )
        # Only add an __init__.py when the source package has none, so the
        # user's own __init__.py is never replaced.
        run(
            output_file,
            os.path.join(source_dir, yaml_file),
            validation_module,
            create_init=add_missing_init and not os.path.exists(source_init),
        )
        outputs.append(output_file)
    return outputs


def _replace_outputs(command, kind, outputs):
    """Delete the files the previous ``kind`` run generated that outputs no longer has.

    A module whose YAML was renamed or removed from setup.py would otherwise
    stay next to the package's own files and keep being installed or imported.
    Only files listed in the record are deleted, so user files are never touched.
    """
    record = os.path.join(
        command.get_finalized_command('build').build_base,
        f'generate_parameter_library_{kind}.txt',
    )
    outputs = [os.path.abspath(output) for output in outputs]
    if os.path.exists(record):
        with open(record) as f:
            for stale in set(f.read().splitlines()) - set(outputs):
                if os.path.exists(stale):
                    os.remove(stale)
    os.makedirs(os.path.dirname(record), exist_ok=True)
    with open(record, 'w') as f:
        f.write('\n'.join(outputs))


def _source_package_root(command):
    source_dir = _source_dir(command.distribution)
    return lambda pkg: os.path.join(source_dir, command.get_package_dir(pkg))


def parameter_cmdclass(
    module_name=None, yaml_file=None, validation_module='', package=None, modules=None
):
    """
    Return setuptools command classes that generate parameter modules.

    Pass the result as ``setup(cmdclass=...)``. Give one module through the
    positional arguments, or several through ``modules``, a list of dicts with
    the keys ``module_name``, ``yaml_file`` and optionally ``validation_module``
    and ``package``.

    ``yaml_file`` is relative to the directory holding setup.py. ``package`` is
    the Python package the module is generated into; it defaults to the yaml
    file's directory when that is a package, else to the distribution name.
    Regular builds generate into the build tree, so the module is installed
    with the rest of the package. Editable installs (``colcon build
    --symlink-install``, ``pip install -e``) generate into the source package,
    which is the copy Python imports in that mode; ``develop --uninstall``,
    which colcon runs when such a build is rebuilt without
    ``--symlink-install``, removes them from there again. A module that is no
    longer generated, e.g. after renaming it, is removed on the next build.
    """
    if modules is None:
        modules = [
            {
                'module_name': module_name,
                'yaml_file': yaml_file,
                'validation_module': validation_module,
                'package': package,
            }
        ]
    elif module_name or yaml_file or validation_module or package:
        raise ValueError(
            'Pass either module_name, yaml_file, validation_module and package, '
            'or modules.'
        )
    specs = [
        (
            module['module_name'],
            module['yaml_file'],
            module.get('validation_module', ''),
            module.get('package'),
        )
        for module in modules
    ]

    class BuildPy(build_py):
        def run(self):
            super().run()
            if getattr(self, 'editable_mode', False):
                # PEP 660 editable wheel: the source tree is what gets imported.
                # The generated files live there, so they stay out of get_outputs().
                generated = _generate(
                    self, specs, _source_package_root(self), add_missing_init=False
                )
                _replace_outputs(self, 'source', generated)
                return
            self._generated = _generate(
                self,
                specs,
                lambda pkg: os.path.join(self.build_lib, *pkg.split('.')),
                add_missing_init=True,
            )
            _replace_outputs(self, 'build_lib', self._generated)

        def get_source_files(self):
            # sdist collects its pure-Python inputs from here.
            return super().get_source_files() + [
                yaml_file for _, yaml_file, _, _ in specs
            ]

        def get_outputs(self, *args, **kwargs):
            return super().get_outputs(*args, **kwargs) + getattr(
                self, '_generated', []
            )

    class Develop(develop):
        def run(self):
            build_py_cmd = self.get_finalized_command('build_py')
            package_root = _source_package_root(build_py_cmd)
            if self.uninstall:
                # colcon runs `develop --uninstall` when a --symlink-install
                # build is rebuilt without it; a module left in the source tree
                # would shadow the installed one wherever the source is on
                # sys.path, e.g. in `colcon test`.
                for spec in specs:
                    _, output_file = _output_file(build_py_cmd, spec, package_root)
                    if os.path.exists(output_file):
                        os.remove(output_file)
                _replace_outputs(build_py_cmd, 'source', [])
            else:
                generated = _generate(
                    build_py_cmd, specs, package_root, add_missing_init=False
                )
                _replace_outputs(build_py_cmd, 'source', generated)
            super().run()

    return {'build_py': BuildPy, 'develop': Develop}


def generate_parameter_module(
    module_name, yaml_file, validation_module='', install_base=None, merge_install=False
):
    # TODO there must be a better way to do this. I need to find the build directory so I can place the python
    # module there
    build_dir = None
    install_dir = None
    for i, arg in enumerate(sys.argv):
        # Look for the `--build-directory` option in the command line arguments
        if arg == '--build-directory' or arg == '--build-base':
            build_arg = sys.argv[i + 1]

            path_split = os.path.split(build_arg)
            path_split = os.path.split(path_split[0])
            pkg_name = path_split[1]
            path_split = os.path.split(path_split[0])
            colcon_ws = path_split[0]

            tmp = sys.version.split()[0]
            tmp = tmp.split('.')
            py_version = f'python{tmp[0]}.{tmp[1]}'

            if not install_base:
                install_base = os.path.join(colcon_ws, 'install')

            install_base = (
                install_base if merge_install else os.path.join(install_base, pkg_name)
            )
            install_dir = os.path.join(
                install_base,
                'lib',
                py_version,
                'site-packages',
                pkg_name,
            )
            build_dir = os.path.join(colcon_ws, 'build', pkg_name, pkg_name)
            break

    if build_dir:
        run(os.path.join(build_dir, module_name + '.py'), yaml_file, validation_module)
    if install_dir:
        run(
            os.path.join(install_dir, module_name + '.py'), yaml_file, validation_module
        )
