# file: base.py
# content: App class definition
# created: 2020 March 21
# modified: 2025 April 22
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

#####################################################################
#                                                     ### DESCRIPTION
#
_DESCRIPTION = """   
    
    --- motivation ---

    This is a mini-library to simplify GUI programming.
    The base module is used to create the main window
    and start the main application.

    --- technically ---

    On instantiating an "App" object, a frame is
    automatically created and a panel container is
    created too that fills the frame window.

    A "BackgroundBitmap" is instantiated and is used to
    paint the panel background. This "BackgroundBitmap"
    is used by default as the canvas for the "layout"
    class to draw all the app's decorations.

    --- requirements ---

    The module "base" requires the module "tools" to be
    present and the package "wxpython" to be installed.

"""

#####################################################################
#                                                         ### HISTORY
# The only available versions is "0.00"
#
_HISTORY = {

    "0.00": """
        Add 'app' class:
            
            . 'app.__init__()' doesn't require any parameters.

            . 'app.Start()', which must be overloaded by the user,
            is used to initialise the user part of the app.
            'app.Start()' is called automatically after the 'main
            Window', the 'main Frame', and the 'main Panel' have
            been instantiated.
            
            . 'app.Run()' is used to run the app and must be called
            by the user after the app instantiation.

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
# . ESCAPE  : enable the escape key for exiting the app
#
from tools import debug_class
_debug = debug_class(
    # 'ALL',
    # 'NONE',
    'VERBOSE',  # only performed when __main__
    'TESTS',    # only performed when __main__
    'LOG',
    'ESCAPE',
    )

#####################################################################
#                                                             ### LOG
# The default log file is 'base.py.log'
# Use the debugging 'LOG' flag to activate messages logging.
#
from tools import log_class
_log = log_class("./base.py.log" if _debug.flag('LOG') else "")

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

# from wxpython: https://www.wxpython.org/

# classes
from wx import Panel                as _wxPanel
from wx import Frame                as _wxFrame
from wx import App                  as _wxApp

# wx classes default constants
from wx import ID_ANY               as _wxID_ANY
from wx import DefaultPosition      as _wxDefaultPosition
from wx import DefaultSize          as _wxDefaultSize
from wx import NO_BORDER            as _wxNO_BORDER
from wx import DEFAULT_FRAME_STYLE  as _wxDEFAULT_FRAME_STYLE
from wx import RESIZE_BORDER        as _wxRESIZE_BORDER
from wx import MAXIMIZE_BOX         as _wxMAXIMIZE_BOX

# wx bitmap methods
from wx import PaintDC as _wxPaintDC

# wx event constants
from wx import EVT_PAINT            as _wxEVT_PAINT
from wx import EVT_KEY_DOWN         as _wxEVT_KEY_DOWN
from wx import WXK_ESCAPE           as _wxWXK_ESCAPE
from wx import EVT_ERASE_BACKGROUND as _wxEVT_ERASE_BACKGROUND

# wx system
from wx import Exit                 as _wxExit

#####################################################################
#                                                         ### LIBRARY

# Quick Panel
class _basePanel(_wxPanel):

    def __init__(self, parent):

        _wxPanel.__init__(
            self,
            parent = parent,
            id     = _wxID_ANY,
            pos    = _wxDefaultPosition,
            size   = _wxDefaultSize,
            style  = _wxNO_BORDER,
            name   = "")

        # BackgroundBitmaps are used to draw decors
        self.BackgroundBitmap = None

        # bind paint event
        # self.Bind(_wxEVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(_wxEVT_PAINT, self._OnPaint)

        # done
        return

    def _onEraseBackground(self, event):
        # force bypass to avoid flicker
        pass

    def _OnPaint(self, event):

        # re-draw BackgroundBitmap if defined
        if self.BackgroundBitmap: 

            # "DCPaint" is used here.
            # but maybe "BufferedPaintDC" should be used instead?
            dc = _wxPaintDC(self)
            dc.DrawBitmap(self.BackgroundBitmap, 0, 0)

        #done
        return

# Quick Frame
class _baseFrm(_wxFrame):

    def __init__(self):

        _wxFrame.__init__(
            self,
            parent = None,
            id     = _wxID_ANY,
            title  = "",
            pos    = _wxDefaultPosition,
            size   = _wxDefaultSize,
            style  = _wxDEFAULT_FRAME_STYLE
                    ^ _wxRESIZE_BORDER
                    ^ _wxMAXIMIZE_BOX,
            name   = "")

        # create the panel
        # (by default the Panel should
        # take the size of the Frame)
        self.Panel = _basePanel(self)

        # done
        return

# When the ESCAPE flag is set you can use the
# ESCAPE key to quit the Application. this is
# used for a quick exit and debugging purposes.
 
# Quick App
class app(_wxApp):

    def OnInit(self):
        # create reference to App
        # self.App = self (most likely useless)
        # create and show Frame
        self.Frame = _baseFrm()     
        # create reference to Panel
        self.Panel = self.Frame.Panel
        # call user's start up code
        self.Start()
        # adjust widow size to BackgroundBitmap size
        if self.Frame.Panel.BackgroundBitmap:
            w, h = self.Frame.Panel.BackgroundBitmap.GetSize()
            self.Frame.SetClientSize((w, h))
        # bind key events
        self.Bind(_wxEVT_KEY_DOWN, self._OnKeyDown)
        # show the frame
        self.Frame.Show(True)
        # done
        return True

    # Start() is to be overloaded by the user
    def Start(self):
        # user's start up code
        pass

    def Run(self):
        self.MainLoop()
        return

    # the following can be overwritten by 
    def _OnKeyDown(self, event):
        
        key = event.GetKeyCode()

        # catch the ESCAPE key and exit
        # the app when the ESCAPE flag
        # is set.

        if _debug.flag("escape"):
            if key == _wxWXK_ESCAPE:
                _log.print('escape pressed: exiting...')
                _wxExit()
                return

        event.Skip() # forward event

        # done
        return

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

            # instantiate and run the app
            a = app()
            a.Run()

        if _test.flag('X.XX'):
            _log.print(" . running test for version X.XX")

_log.boxprint('done')
