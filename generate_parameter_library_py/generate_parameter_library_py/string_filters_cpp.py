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

import json


def valid_string_cpp(description):
    """
    Filter a string to make it a valid C++ string literal.

    Args:
      description (str): The input string to be filtered.

    Returns:
      str: The filtered string that is a valid C++ string.
    """
    if description:
        # remove possible markdown/rst syntax, but add proper indent for cpp-header files.
        filtered_description = (
            description.replace('\\', '\\\\')
            .replace('`', '')
            .replace('\n', '\\n    ')
            .replace('"', '\\"')
        )
        return f'"{filtered_description}"'
    else:
        return '""'


def valid_string_python(description):
    """
    Escape a string for use between the double quotes of a Python string literal.

    Backslashes, quotes and control characters are escaped, and each newline is
    followed by an indent, as valid_string_cpp does.

    Args:
      description (str): The input string to be filtered.

    Returns:
      str: The escaped text without the surrounding quotes, or '' when the
      input is empty.
    """
    if description:
        # The templates add the quotes; JSON escaping without them is valid
        # inside a Python string literal.
        return json.dumps(description.replace('\n', '\n    '), ensure_ascii=False)[1:-1]
    else:
        return ''
