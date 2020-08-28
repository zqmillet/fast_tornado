"""
description: this module contains testcases about constants of fast_torrnado.
author: qiqi
"""

import os
import re

from fast_torrnado import VERSION
from fast_torrnado import ROOT

def test_root():
    assert os.path.isdir(ROOT)

def test_version():
    assert VERSION.startswith('v')
    assert re.match(r'^v\d+\.\d+\.\d+$', VERSION) is not None
