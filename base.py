# file: base.py
# content: App class definition
# created: 2020 March 21
# modified: 2025 April 14
# author: Roch Schanen
# repository:
# comment:

# CONFIGURATION

_LOG_FILE = "tmp.log"

_DEBUG_FLAGS = [
    # 'ALL',
    # 'NONE',
    'LOG',
]

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

    --- additional features ---

    additional functions are included that help to debug
    and log some data. 

"""

# LOGGING

def debug(*flags):
    if "NONE" in _DEBUG_FLAGS: return False
    if "ALL"  in _DEBUG_FLAGS: return True
    for f in flags:
        if f.upper() in _DEBUG_FLAGS:
            return True
    if flags: # no valid flags
        return False
    # an empty set of parameter always returns True
    # use 'NONE' to bypass all debug messages
    return True

_LOG_FILE_HANDLE = None
if debug('LOG'): _LOG_FILE_HANDLE = open(_LOG_FILE, "w")

def lprint(*args, **kwargs):
    print(*args, **kwargs)
    if _LOG_FILE_HANDLE is None: return
    kwargs["file"] = _LOG_FILE_HANDLE
    print(*args, **kwargs)
    return

# DISPLAY FILE HEADER

def header():

    lprint()
    lprint(f"┌─────────────┐")
    lprint(f"│ file header │")
    lprint(f"└─────────────┘")
    lprint()

    from os.path import realpath
    from sys import argv

    # get main script content
    fp = realpath(argv[0])  # file path
    fh = open(fp, 'r')      # file handle
    ft = fh.read()          # file text
    fh.close()              # done

    # print every lines while they begin with #
    L = ft.split('\n')
    for l in L[1:]:
        if not l: break
        if not l[0]=="#": break
        lprint(l)

    # done
    return

# DISPLAY PYTHON VERSION

def python_version():
    from sys import version
    lprint()
    lprint(f"┌────────────────┐")
    lprint(f"│ python version │")
    lprint(f"└────────────────┘")
    lprint()
    lprint(f"run Python version {version.split(' ')[0]}")
    return

# DISPLAY VERSION HISTORY

_VERSION_HISTORY = {}

def version_history():

    version = list(_VERSION_HISTORY.keys())[-1]

    lprint()
    lprint(f"┌────────────────┐")
    lprint(f"│ module version │")
    lprint(f"└────────────────┘")
    lprint()
    lprint(f"module version is '{version}'")

    lprint()
    lprint(f"┌──────────────────┐")
    lprint(f"│ versions history │")
    lprint(f"└──────────────────┘")
    
    for v in _VERSION_HISTORY.values():
        lprint(v)

    return version

# all constants, methods and classes are imported
# individually to clarify the usage of packages.

# from wxpython: https://www.wxpython.org/

# classes
from wx import Panel                as wxPanel
from wx import Frame                as wxFrame
from wx import App                  as wxApp

# wx classes default constants
from wx import ID_ANY               as wxID_ANY
from wx import DefaultPosition      as wxDefaultPosition
from wx import DefaultSize          as wxDefaultSize
from wx import NO_BORDER            as wxNO_BORDER
from wx import DEFAULT_FRAME_STYLE  as wxDEFAULT_FRAME_STYLE
from wx import RESIZE_BORDER        as wxRESIZE_BORDER
from wx import MAXIMIZE_BOX         as wxMAXIMIZE_BOX

# wx bitmap methods
from wx import PaintDC as wxPaintDC

# wx event constants
from wx import EVT_PAINT            as wxEVT_PAINT
from wx import EVT_KEY_DOWN         as wxEVT_KEY_DOWN
from wx import WXK_ESCAPE           as wxWXK_ESCAPE
from wx import EVT_ERASE_BACKGROUND as wxEVT_ERASE_BACKGROUND

# wx system
from wx import Exit                 as wxExit

# Quick Panel
class _basePanel(wxPanel):

    def __init__(self, parent):

        wxPanel.__init__(
            self,
            parent = parent,
            id     = wxID_ANY,
            pos    = wxDefaultPosition,
            size   = wxDefaultSize,
            style  = wxNO_BORDER,
            name   = "")

        # BackgroundBitmaps are used to draw decors
        self.BackgroundBitmap = None

        # bind paint event
        # self.Bind(wxEVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(wxEVT_PAINT, self._OnPaint)

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
            dc = wxPaintDC(self)
            dc.DrawBitmap(self.BackgroundBitmap, 0, 0)

        #done
        return

# Quick Frame
class _baseFrm(wxFrame):

    def __init__(self):

        wxFrame.__init__(
            self,
            parent = None,
            id     = wxID_ANY,
            title  = "",
            pos    = wxDefaultPosition,
            size   = wxDefaultSize,
            style  = wxDEFAULT_FRAME_STYLE
                    ^ wxRESIZE_BORDER
                    ^ wxMAXIMIZE_BOX,
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
class app(wxApp):

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
        self.Bind(wxEVT_KEY_DOWN, self._OnKeyDown)
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

    def _OnKeyDown(self, event):
        
        key = event.GetKeyCode()

        # catch the ESCAPE key and exit the app
        # when the _ESCAPE flag is set. This is
        # used for development purposes. It will
        # be removed at later time.

        if _ESCAPE:
            if key == wxWXK_ESCAPE:
                wxExit()
                return

        event.Skip() # forward event

        # done
        return

_VERSION_HISTORY["0.0"] = """
version 0.0 (21 March 2020 - 14 April 2025):

    classes:
        
        . _basePanel(parent)        
        
        . _baseFrm()
        
        . app()
            app.Start()
            app.Run()

    functions:

        . header()
        . python_version()

    constants:

        . _ESCAPE = True
"""

if __name__ == "__main__":

    header()
    python_version()
    version = version_history()

    # test list
    TESTS = [
        version,
        # "0.0",
        # "x.x",
        ]

    #############
    # tests 0.0 #
    #############

    if "0.0" in TESTS:

        lprint()
        lprint(f"┌──────┐")
        lprint(f"│ TEST │")
        lprint(f"└──────┘")
        lprint()
        lprint("running test version 0.0")

        a = app()
        a.Run()
