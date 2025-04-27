# file: elements.py
# content: 
# created: 2025 April 27
# modified: 2025 April 27
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

#####################################################################
#                                                     ### DESCRIPTION
_DESCRIPTION = """   
"""

#####################################################################
#                                                         ### HISTORY
_HISTORY = {

    "0.00": """
        add display()
    """,
    
    }

#####################################################################
#                                                           ### DEBUG
from tools import debug_class
_debug = debug_class(
    # 'ALL',
    # 'NONE',
    # 'VERBOSE',
    'TESTS',
    'LOG',
    )

#####################################################################
#                                                             ### LOG
from tools import log_class
_log = log_class(
    "./logs/elements.py.log" if _debug.flag('LOG') else ""
    )

#####################################################################
#                                                            ### TEST
if _debug.flag('TESTS'):
    _test = debug_class(
        sorted(_HISTORY)[-1],
        )

#####################################################################
#                                                         ### IMPORTS
# from wxpython: https://www.wxpython.org/
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
#                                                         ### LIBRARY
class Display(_wxControl):
    
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

            from base   import app
            from theme  import images

            # derive a new class from app
            class myapp(app):

                def Start(self):

                    # instanciate image library
                    library = images()
                    
                    # load background bitmap (all of the images)
                    library.load('bkgd')

                    # use background bitmap
                    self.Panel.BackgroundBitmap = library.select('bkgd')
                    
                    # load led bitmaps (blue and red only)
                    library.load('leds', ['red', 'blue'])

                    led1 = Display(
                        self.Panel,
                        library.select('leds', 'red', ['on', 'off']),
                        ['on', 'off'])
                    led1.SetPosition((100, 100))
                    led1.SetValue('on')
                    
                    led2 = Display(
                        self.Panel,
                        library.select('leds', 'blue', ['off', 'on']),
                        ['off', 'on'])
                    led2.SetPosition((130, 100))
                    led2.SetValue(1)

                    # done
                    return
            
            m = myapp()
            m.Run()

            _log.print(" . end test for version 0.00")
