# file: elements.py
# content: 
# created: 2025 April 27
# modified: 2025 April 27
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

_LOGFILE = \
    f"./logs/elements.py.log"

_FLAGS = [
    'TESTS',
    'LOG',
    ]

_TESTS = [
    '0.00',
    '0.01',
    ]

from tools import debug_class
_debug = debug_class(*_FLAGS)
from tools import log_class
_log = log_class(_LOGFILE if _debug.flag('LOG') else "")
if _debug.flag('TESTS'): _test = debug_class(*_TESTS)

#####################################################################
#                            IMPORTS
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

# _btn
from wx import EVT_LEFT_DOWN            as _wxEVT_LEFT_DOWN
from wx import EVT_LEFT_DCLICK          as _wxEVT_LEFT_DCLICK
from wx import PostEvent                as _wxPostEvent
from wx.lib.newevent import NewEvent    as _wxNewEvent

# Push
from wx import EVT_LEFT_UP              as _wxEVT_LEFT_UP
from wx import EVT_LEAVE_WINDOW         as _wxEVT_LEAVE_WINDOW

#####################################################################
#                             display

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
#                              _btn

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
#                               push

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

#####################################################################

if __name__ == "__main__":
    if _debug.flag('tests'):
        if _test.flag('0.00'):

            if _debug.flag('verbose'):
                _log.boxprint('verbose')
                _log.os_version()
                _log.python_version()
                _log.file_header()
                _log.history(_HISTORY)
            
            _log.boxprint('tests')
            _log.print(" . running test for version 0.00")

            from base   import app
            from theme  import images

            # derive a new class from app
            class myapp(app):

                def push_handler(self, event):
                    _log.print(f'push pressed...')
                    return

                def Start(self):
                    # instanciate image library
                    library = images()
                    # load background bitmap (all of the images)
                    library.load('bkgd')
                    # use background bitmap
                    self.Panel.BackgroundBitmap = library.select('bkgd')
                    # load led bitmaps (blue and red only)
                    library.load('leds', ['red', 'blue'])
                    # led 1
                    led1 = display(
                        self.Panel,
                        library.select('leds', 'red', ['on', 'off']),
                        ['on', 'off'])
                    led1.SetPosition((100, 100))
                    led1.SetValue('on')
                    # led 2
                    led2 = display(
                        self.Panel,
                        library.select('leds', 'blue', ['off', 'on']),
                        ['off', 'on'])
                    led2.SetPosition((130, 100))
                    led2.SetValue(1)
                    # load push button
                    library.load('push', 'blank')
                    # push 1
                    push1 = push(
                        self.Panel,
                        library.select(
                            'push',
                            ['released', 'pressed'],
                            ),
                        )
                    push1.SetPosition((160, 100))
                    push1.BindEvent(self.push_handler)                    
                    # done
                    return
            
            m = myapp()
            m.Run()

            _log.print(" . end test for version 0.00")
