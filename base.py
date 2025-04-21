# file: base.py
# content: App class definition
# created: 2020 March 21
# modified: 2025 April 21
# author: Roch Schanen
# repository:
# comment:

""" 
    --- motivation ---

    This is a mini-library to simplify GUI programing.
    The base module is used to create the main window
    and start the main application.

    --- technically ---

    On instantiating an "App" object, a frame is
    automatically created and a panel container is
    created too that fills the frame window.

    A "BackgroundBitmap" is instantiated and is used to
    paint the panel background. This "BackgroundBitmap"
    is used by default as a canvas for the layout class
    to draw the app's decorations.

    --- requirements ---

    tools, wxpython.

"""

from tools import *

#####################################################################
#                                                           ### DEBUG
debug = debug_class(
    # 'ALL',
    # 'NONE',
    # 'LOG',
    'VERBOSE',
    'ESCAPE',
    )

#####################################################################
#                                                             ### LOG

log = log_class("./base.py.log" if debug.flag('LOG') else "")

#####################################################################
#                                                         ### HISTORY
_HISTORY = {

    ### VERSION 0.00

    "0.00": """
    content:

        . app()
            app.Start()
            app.Run()
        """,
}

#####################################################################
#                                                    ### SELECT TESTS

TESTS = [
    # "X.XX",               # run test for version X.XX
    sorted(_HISTORY)[-1],   # run test for last version
    ]

#####################################################################
#                                                         ### IMPORTS

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
# used for debbugging purposes.
 
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

        if debug.flag("escape"):
            if key == _wxWXK_ESCAPE:
                _wxExit()
                return

        event.Skip() # forward event

        # done
        return

#####################################################################
#                                                           ### TESTS

if __name__ == "__main__":

    if debug.flag('LOG'):
        
        if debug.flag('VERBOSE'):
            log.display_file_header()
            log.display_os_version()
            log.display_python_version()
            log.display_history(_HISTORY)

    #############
    # tests 0.0 #
    #############

    if "0.00" in TESTS:

        if debug.flag('LOG'):
            log.boxprint(f"TEST")
            log.print("running test version 0.00")

        a = app()
        a.Run()

    if "1.00" in TESTS:

        if debug.flag('LOG'):
            log.boxprint(f"TEST")
            log.print("running test version 1.00")

        a = app()
        a.Run()
