# file: theme.py
# content: image collection manager
# created: 2025 April 22
# modified: 2025 April 22
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

#####################################################################
#                                                     ### DESCRIPTION
#
_DESCRIPTION = """   
    
    --- motivation ---

        This is a library to help retrieve image collections from a
        set of png files and to filter and select groups of images
        from the collections that are to be used for background,
        buttons, switches, etc.

"""

#####################################################################
#                                                         ### HISTORY
# The only available versions is "0.00"
#
_HISTORY = {

    "0.00": """
        . add ImageCollection()

    """,
}

#####################################################################
#                                                           ### DEBUG
# uncomment line to set any flag:
#
# . NONE    : clears all flags (precedes the 'ALL' flag)
# . ALL     : sets all flags (all flags are selected except 'NONE')
# . LOG     : log messages to file
# . VERBOSE : display extra informations
# . TEST    : enable the selected tests
#
from tools import debug_class
_debug = debug_class(
    # 'ALL',
    # 'NONE',
    # 'VERBOSE',  # only performed when __main__
    'TESTS',    # only performed when __main__
    'LOG',
    )

#####################################################################
#                                                             ### LOG
# The default log file is 'theme.py.log'
# Use the debugging 'LOG' flag to activate messages logging.
#
from tools import log_class
_log = log_class("./theme.py.log" if _debug.flag('LOG') else "")

#####################################################################
#                                                            ### TEST
#
if _debug.flag('TESTS'):
    _test = debug_class(
        sorted(_HISTORY)[-1],   # run last version
        # "X.XX",               # run version X.XX
        )

#####################################################################
#                                                         ### IMPORTS
#
# all constants, methods and classes are imported
# individually to clarify the usage of packages.
#

# from standard packages:
from sys        import path             as _path
from os.path    import isfile           as _isfile

# from wxpython: https://www.wxpython.org/
# wx bitmap methods
from wx import Bitmap                   as _wxBitmap
from wx import BITMAP_TYPE_PNG          as _wxBITMAP_TYPE_PNG
from wx import Rect                     as _wxRect

#####################################################################
#                                                         ### LIBRARY
#








#####################################################################
#                                                           ### TESTS
#
if __name__ == "__main__":

    if _debug.flag('verbose'):

        _log.boxprint('verbose')
        _log.os_version()
        _log.python_version()
        _log.file_header()
        _log.history(_HISTORY)

    if _debug.flag('tests'):
        _log.boxprint('tests')

        if _test.flag('0.00'):
            _log.print(" . running test for version 0.00")

            from base import app

            # derive a new class from app
            class myapp(app):

                def Start(self):
                    # # collect images from "Panels.png"
                    # img = imageCollect("panels", "large")
                    # # manually setup the background image of myapp
                    # self.Panel.BackgroundBitmap = img
                    # done
                    return
            
            # instanciate myapp
            m = myapp()

            # run myapp
            m.Run()

_log.boxprint('done')
