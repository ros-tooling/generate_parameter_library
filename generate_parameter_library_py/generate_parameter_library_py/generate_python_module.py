#!/usr/bin/env python3

# Copyright 2022 PickNik Inc.
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

import argparse
import sys
import os

from generate_parameter_library_py.parse_yaml import GenerateCode


def run(output_file, yaml_file, validation_module='', create_init=True):
    print(f'Running {__file__} {output_file} {yaml_file} {validation_module}')
    gen_param_struct = GenerateCode('python')
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    gen_param_struct.parse(yaml_file, validation_module)

    code = str(gen_param_struct)
    with open(output_file, 'w') as f:
        f.write(code)

    # Put an __init__.py file if one does not yet exist.
    if create_init:
        init_file = os.path.join(os.path.dirname(output_file), '__init__.py')
        open(init_file, 'a').close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_python_module_file')
    parser.add_argument('input_yaml_file')
    parser.add_argument('validate_file', nargs='?', default='')
    return parser.parse_args()


def main():
    args = parse_args()
    output_file = args.output_python_module_file
    yaml_file = args.input_yaml_file
    validate_file = args.validate_file
    run(output_file, yaml_file, validate_file)


if __name__ == '__main__':
    sys.exit(main())
