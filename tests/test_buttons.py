# file: test_tools.py
# content: debug and logging tools
# created: 2025 April 17
# modified: 2025 April 30
# author: Roch Schanen
# repository: https://github.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

_LOG_FILE = f".logs/test_tools.py.log"

_DEBUG_FLAGS = [
    # 'NONE',
    # 'ALL',
    # 'VERBOSE',
    'log',
    'tests',
    'import',
    ]

_TEST_FLAGS = [
    'push',
    ]

#####################################################################

if 'import' in _DEBUG_FLAGS: # test the un-installed package
    import sys
    sys.path.insert(1, '..')

from ULT_FRIDGE6_MONITOR.tools import debug_class
_debug = debug_class(*_DEBUG_FLAGS)

from ULT_FRIDGE6_MONITOR.tools import log_class
_log = log_class(_LOG_FILE if _debug.flag('LOG') else "")

if _debug.flag('TESTS'):
    _test = debug_class(*_TEST_FLAGS)

#####################################################################
#                                                                leds

if _test.flag('push'):

    _log.print(" . start test push button")

    from ULT_FRIDGE6_MONITOR.base       import app
    from ULT_FRIDGE6_MONITOR.theme      import images
    from ULT_FRIDGE6_MONITOR.buttons    import push

    # derive a new class from app
    class myapp(app):

        def push1_handler(self, event):
            _log.print(f'push pressed...')
            return

        # setup app using Start()
        def Start(self):
            
            # instanciate image library
            self.library = images()
            # load background bitmaps
            self.library.load('bkgd')
            # load push button (the blank style)
            self.library.load('push', 'blank')
            
            # use background bitmap
            # (only one image image definition in 'bkdg')
            self.Panel.BackgroundBitmap = self.library.select('bkgd')

            # push 1
            self.push1 = push(
                self.Panel,
                self.library.select(
                    'push',
                    ['released', 'pressed'],
                    ),
                )
            # set button position
            self.push1.SetPosition((160, 100))
            
            # bind call back function
            self.push1.BindEvent(self.push1_handler)                    

            # done
            return
    
    # instantiate app
    m = myapp()

    # run app
    m.Run()

    # done
    _log.print(" . end test push button")
