"""
description: this module provides the function ``wrap_text``.
"""

import textwrap
import shutil

def wrap_text(text, indent=0, wrap=True, width=None):
    """
    description: this function is used to wrap text.
    """
    if not width:
        width = shutil.get_terminal_size().columns

    if wrap:
        text = '\n'.join(textwrap.wrap(text, width - indent))

    return textwrap.indent(text, indent * ' ')
