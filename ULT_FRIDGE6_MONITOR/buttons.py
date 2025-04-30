# file: elements.py
# content: 
# created: 2025 April 27
# modified: 2025 April 30
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

_LOG_FILE = f".logs/buttons.py.log"

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

# _btn
from wx import EVT_LEFT_DOWN            as _wxEVT_LEFT_DOWN
from wx import EVT_LEFT_DCLICK          as _wxEVT_LEFT_DCLICK
from wx import PostEvent                as _wxPostEvent
from wx.lib.newevent import NewEvent    as _wxNewEvent

# Push
from wx import EVT_LEFT_UP              as _wxEVT_LEFT_UP
from wx import EVT_LEAVE_WINDOW         as _wxEVT_LEAVE_WINDOW

from ULT_FRIDGE6_MONITOR.displays import display

#####################################################################
#                                                                _btn

class _btn(display):

    def __init__(self, parent, images, names = None):

        display.__init__(self, parent, images, names)

        # locals
        self.radio = None
        self.ctr   = None
        self.evt   = None

        # bindings
        self.Bind(_wxEVT_LEFT_DOWN,   self._onMouseDown)

        # capture double clicks events as secondary single clicks
        self.Bind(_wxEVT_LEFT_DCLICK, self._onMouseDown)

        # call child _start() method
        self._start()

        # done
        return

    def _start(self):
        pass

    # radio feature
    def _clear(self):
        pass

    # on EVT_LEFT_DOWN, the event.skip()
    # method must be called to preserve
    # the focus event to be processed
    def _onMouseDown(self, event):
        event.Skip() # allow focus events
        return

    # Bind the event to the parent handler
    def BindEvent(self, handler):
        # "handler" is a reference to the handler method
        # usually defined by the parent class
        self.ctr, self.evt = _wxNewEvent()
        self.GetParent().Bind(self.evt, handler)
        return

    # Sends a event to parent using "status" as parameter
    def SendEvent(self):
        if self.ctr:
            event = self.ctr(caller=self, status=self.status)
            _wxPostEvent(self.GetParent(), event)
        return

#####################################################################
#                                                                push

class push(_btn):

    def _start(self):
        self.lock = False
        self.Bind(_wxEVT_LEFT_UP,      self._onMouseUp)
        self.Bind(_wxEVT_LEAVE_WINDOW, self._onMouseLeave)
        return

    def _onMouseDown(self, event):
        event.Skip() # allow focus events
        self.lock = True
        if self.radio:
            self.radio.Select(self)
        self.status = 1
        self.Refresh()
        self.SendEvent()
        return

    def _onMouseUp(self, event):
        if self.lock:
            self.lock = False
            self.status = 0
            self.Refresh()
        return

    def _onMouseLeave(self, event):
        if self.lock:
            self.lock = False
            self.status = 0
            self.Refresh()
        return
