"""
description: this module contains testcases about constants of fast_torrnado.
author: qiqi
"""

import os
import re

from fast_torrnado import VERSION
from fast_torrnado import ROOT

def test_root():
    """
    description: test the constant ROOT does exist.
    steps:
        - assert ROOT is a directory.
    """
    assert os.path.isdir(ROOT)

def test_version():
    """
    description: test the format of VERSION is right.
    steps:
        - assert VERSION is match the regex.
    """
    assert re.match(r'^v\d+\.\d+\.\d+$', VERSION) is not None
