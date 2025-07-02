# file: container.py
# content: Control class definition
# created: 2020 April 03
# modified: 2025 April 04
# modification:
# author: Roch Schanen
# repository: https://github.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

_LOG_FILE = f"../tests/.logs/container.py.log"

_DEBUG_FLAGS = [
    # 'NONE',
    # 'ALL',
    # 'VERBOSE',
    # 'LOG',
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

# wxpython: https://www.wxpython.org/

# container
from wx import Control                  as _wxControl
from wx import ID_ANY                   as _wxID_ANY
from wx import DefaultPosition          as _wxDefaultPosition
from wx import DefaultSize              as _wxDefaultSize
from wx import NO_BORDER                as _wxNO_BORDER
from wx import DefaultValidator         as _wxDefaultValidator
from wx import EVT_ERASE_BACKGROUND     as _wxEVT_ERASE_BACKGROUND
from wx import EVT_PAINT                as _wxEVT_PAINT
from wx import BufferedPaintDC          as _wxBufferedPaintDC
from wx.lib.newevent import NewEvent    as _wxNewEvent
from wx import PostEvent                as _wxPostEvent

#####################################################################
#                                                           container

class container(_wxControl):

    def __init__(
        self,
        parent):

        _wxControl.__init__(
            self,
            parent      = parent,
            id          = _wxID_ANY,
            pos         = _wxDefaultPosition,
            size        = _wxDefaultSize,
            style       = _wxNO_BORDER,
            validator   = _wxDefaultValidator,
            name        = "")

        # parameters
        self.parent = parent

        # status is the value returned
        # by SendEvent to owner class
        self.status = None
        
        # When defined the BackgroundBitmap
        # is automatically re-drawn on any
        # paint event
        self.BackgroundBitmap = None
        
        # "self.ctr" is used to build the event
        # object that needs to be returned to
        # the owner. "self.evt" may not need to
        # be defined globally...
        self.ctr, self.evt = None, None
        
        # bindings
        self.Bind(_wxEVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(_wxEVT_PAINT,self._onPaint)
        
        # user constructor
        self.Start()
        
        # done
        return

    def SetBackground(self, Bitmap):
        w, h = Bitmap.GetSize()
        self.SetSize((w, h))
        self.BackgroundBitmap = Bitmap
        return

    # to be overloaded by user's code
    def Start(self):
        pass

    def _onEraseBackground(self, event):
        # force bypass to avoid flicker
        pass

    def _onPaint(self, event):
        if self.BackgroundBitmap:
            dc = _wxBufferedPaintDC(self)
            dc.DrawBitmap(self.BackgroundBitmap, 0, 0)
        return

    def BindEvent(self, handler):
        self.ctr, self.evt = _wxNewEvent()
        self.GetParent().Bind(self.evt, handler)
        return
        # "self.evt" is only used once in the "BindEvent" method
        # can it then be defined only locally?

    def SendEvent(self):
        if self.ctr:
            event = self.ctr(caller=self, status = self.status)
            _wxPostEvent(self.GetParent(), event)
        return