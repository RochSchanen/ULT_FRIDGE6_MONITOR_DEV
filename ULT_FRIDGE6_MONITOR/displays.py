# file: elements.py
# content: 
# created: 2025 April 27
# modified: 2025 April 27
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

_LOG_FILE = f".logs/displays.py.log"

_DEBUG_FLAGS = [
    'NONE',
    # 'ALL',
    # 'VERBOSE',
    # 'LOG',
    ]

if not __name__ == '__main__':

    from ULT_FRIDGE6_MONITOR.tools import debug_class
    _debug = debug_class(*_DEBUG_FLAGS)

    from ULT_FRIDGE6_MONITOR.tools import log_class
    _log = log_class(_LOG_FILE if _debug.flag('LOG') else "")

#####################################################################
#                                                             imports

# from wxpython: https://www.wxpython.org/

# display
from wx import Control                  as _wxControl
from wx import ID_ANY                   as _wxID_ANY
from wx import DefaultPosition          as _wxDefaultPosition
from wx import DefaultSize              as _wxDefaultSize
from wx import NO_BORDER                as _wxNO_BORDER
from wx import DefaultValidator         as _wxDefaultValidator
from wx import EVT_ERASE_BACKGROUND     as _wxEVT_ERASE_BACKGROUND
from wx import EVT_PAINT                as _wxEVT_PAINT
from wx import BufferedPaintDC          as _wxBufferedPaintDC

#####################################################################
#                                                             display

class display(_wxControl):
    
    # superseed __init__()
    def __init__(self, parent, bitmaps, names = None):
        
        # call parent __init__()
        _wxControl.__init__(
            self,
            parent      = parent,
            id          = _wxID_ANY,
            pos         = _wxDefaultPosition,
            size        = _wxDefaultSize,
            style       = _wxNO_BORDER,
            validator   = _wxDefaultValidator,
            name        = "",
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
#                                                             display

