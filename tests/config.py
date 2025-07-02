# file: test-config.py
# content: general configuration for test scripts
# author: Roch Schanen

# get local 
import os
import sys

#  get path to test script
test_path = os.getcwd()

# add path to the package being tested (but not yet installed)
sys.path.insert(1, f"{test_path}\\..")

# make log file path
_LOG_FILE = f".logs/test_tools.py.log"

# DEFAULT DEBUG FLAGS for testing 
_DEBUG_FLAGS = [
    # 'ALL',
    # 'VERBOSE',
    # 'NONE',
    'log',
    'tests',
]


from ULT_FRIDGE6_MONITOR.tools import debug_class
_debug = debug_class(*_DEBUG_FLAGS)

from ULT_FRIDGE6_MONITOR.tools import log_class
_log = log_class(_LOG_FILE if _debug.flag('LOG') else "")

