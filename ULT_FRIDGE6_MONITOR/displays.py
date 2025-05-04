# file: displays.py
# content: 
# created: 2025 April 27
# modified: 2025 April 27
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

_LOG_FILE = f"../tests/.logs/displays.py.log"

_DEBUG_FLAGS = [
    # 'NONE',
    # 'ALL',
    # 'VERBOSE',
    'LOG',
    'import',
    ]

if 'import' in _DEBUG_FLAGS: # un-installed package
    import sys
    sys.path.insert(1, '..')

from ULT_FRIDGE6_MONITOR.tools import debug_class
_debug = debug_class(*_DEBUG_FLAGS)

from ULT_FRIDGE6_MONITOR.tools import log_class
_log = log_class(_LOG_FILE if _debug.flag('LOG') else "")

#####################################################################
#                                                             imports

# from wxpython: https://www.wxpython.org/

# display
from wx import Control              as _wxControl
from wx import ID_ANY               as _wxID_ANY
from wx import DefaultPosition      as _wxDefaultPosition
from wx import DefaultSize          as _wxDefaultSize
from wx import NO_BORDER            as _wxNO_BORDER
from wx import DefaultValidator     as _wxDefaultValidator
from wx import EVT_ERASE_BACKGROUND as _wxEVT_ERASE_BACKGROUND
from wx import EVT_PAINT            as _wxEVT_PAINT
from wx import BufferedPaintDC      as _wxBufferedPaintDC

# fixdisplay
from ULT_FRIDGE6_MONITOR.container import container

#####################################################################
#                                                             display

class display(_wxControl):
    
    # superseed __init__()
    def __init__(self, parent, bitmaps, names = None):
        
        # call parent __init__()
        _wxControl.__init__(
            self,
            parent    = parent,
            id        = _wxID_ANY,
            pos       = _wxDefaultPosition,
            size      = _wxDefaultSize,
            style     = _wxNO_BORDER,
            validator = _wxDefaultValidator,
            name      = "",
            )
        
        # parameters
        self.parent  = parent
        self.bitmaps = bitmaps
        self.names   = names

        # locals

        # status is an index or a name
        self.status = 0
        
        # get png size from first image
        w, h = self.bitmaps[self.status].GetSize()

        # set display size
        self.SetSize((w, h))
        
        # BINDINGS
        self.Bind(_wxEVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(_wxEVT_PAINT, self._onPaint)

        # done
        return

    def _onEraseBackground(self, event):
        # no operation to reduce flicker
        pass 

    def _onPaint(self, event):
        v = self.status
        if isinstance(v, int): n = v
        if isinstance(v, str): n = self.names.index(v)
        dc = _wxBufferedPaintDC(self)
        dc.DrawBitmap(self.bitmaps[n], 0, 0)
        return

    def SetValue(self, Value):
        self.status = Value
        self.Refresh()
        return

    def GetValue(self):
        return self.status

#####################################################################
#                                                          fixdisplay
#

class fixdisplay(container):

    def __init__(
        self, 
        parent,        # parent
        fix,           # fix point format
        bitmaps,       # digits and symbols
        names = None): # digits and symbols
        
        # call parent __init__()
        container.__init__(
            self,
            parent = parent)
        
        # parameters
        self.fix = fix                

        # status is a list of names, one name
        # for each digit and for the dot.
        self.status = list(f"{0:{fix}}")

        # init
        self.D, X, H = [], 0, 0
        # instanciation loop
        for i, s in enumerate(self.status):
            # create
            d = display(self, bitmaps, names)
            # place
            d.SetPosition((X, 0))
            # set default value
            d.SetValue(s)
            # record into list
            self.D.append(d)
            # get current image
            i = bitmaps[names.index(s)]
            # get current size
            w, h = i.GetSize()
            # find maximum height
            if H < h: H = h
            # shift position
            X += w

        # set control size
        self.SetSize(X, H)

        # done
        return

    def SetValue(self, value):
        self.value = value
        self.status = list(f"{value:{self.fix}}")
        for d, s in zip(self.D, self.status):
            d.SetValue(s)
        return            

    def GetValue(self):
        return self.value
