# file: base.py
# content: App class definition
# created: 2020 March 21
# modified: 2025 April 15
# author: Roch Schanen
# repository:
# comment:

_VERSION_HISTORY = {}

from tools import debug_class
debug = debug_class(
    # 'ALL',
    # 'NONE',
    # 'OS',
    'HEADER',
    # 'PYTHON',
    'HISTORY',
    'LOG',
    )

from tools import log_class
log = log_class("./tmp.log")

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

"""

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

# When the constant _ESCAPE = True you can use the
# ESCAPE key to quit the Application. this is used
# for debbugging and should be disabled at later time.
_ESCAPE = True

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

        # catch the ESCAPE key and exit the app
        # when the _ESCAPE flag is set. This is
        # used for development purposes. It will
        # be removed at later time.

        if _ESCAPE:
            if key == _wxWXK_ESCAPE:
                _wxExit()
                return

        event.Skip() # forward event

        # done
        return

_VERSION_HISTORY["0.0"] = """
version  : 0.0
created  : 21 March 2020
modified : 20 April 2025

    classes:

        . app()
            app.Start()
            app.Run()

    hidden classes:
        
        . _basePanel(parent)        
        
        . _baseFrm()
            
    hidden constants:

        . _VERSION_HISTORY['0.0']

        . _ESCAPE 

        . _wxPanel
        . _wxFrame
        . _wxApp
        . _wxID_ANY
        . _wxDefaultPosition
        . _wxDefaultSize
        . _wxNO_BORDER
        . _wxDEFAULT_FRAME_STYLE
        . _wxRESIZE_BORDER
        . _wxMAXIMIZE_BOX
        . _wxPaintDC
        . _wxEVT_PAINT
        . _wxEVT_KEY_DOWN
        . _wxWXK_ESCAPE
        . _wxEVT_ERASE_BACKGROUND
        . _wxExit
"""

if __name__ == "__main__":

    # test list
    TESTS = [
        list(_VERSION_HISTORY.keys())[-1],
        # "1.0",
        # "2.0",
        ]

    if debug.flag('LOG'):
        
        if debug.flag('HEADER'):
            log.display_file_header()
        
        if debug.flag('OS'):
            log.display_os_version()
        
        if debug.flag('PYTHON'):
            log.display_python_version()
        
        if debug.flag('HISTORY'):
            log.display_version_history(_VERSION_HISTORY)

    #############
    # tests 0.0 #
    #############

    if "0.0" in TESTS:

        if debug.flag('LOG'):
            log.boxprint(f"TEST")
            log.print("running test version 0.0")

        a = app()
        a.Run()
