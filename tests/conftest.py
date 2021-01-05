import os
import sys

import pytest
import py._io.terminalwriter
import _pytest.terminal
from py.builtin import text, bytes

current_folder = os.path.dirname(os.path.abspath(__file__))
prev_folder = os.path.dirname(current_folder)
sys.path.append(os.path.join(prev_folder, "ragnaweb"))
sys.path.append(os.path.join(prev_folder, "ragnaweb/src"))
