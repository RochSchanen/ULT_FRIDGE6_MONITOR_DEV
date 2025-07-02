# file: test_tools.py
# content: debug and logging tools
# created: 2025 April 17
# modified: 2025 April 22
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
    'leds',
]

#####################################################################
#                                                              IMPORT
#####################################################################


if 'import' in _DEBUG_FLAGS:    # test the un-installed package
    import sys

exit()

from ULT_FRIDGE6_MONITOR.tools import debug_class
_debug = debug_class(*_DEBUG_FLAGS)

from ULT_FRIDGE6_MONITOR.tools import log_class
_log = log_class(_LOG_FILE if _debug.flag('LOG') else "")

if _debug.flag('TESTS'):
    _test = debug_class(*_TEST_FLAGS)

#####################################################################
#                                                                leds

if _test.flag('leds'):

    _log.print(" . start test leds")

    from ULT_FRIDGE6_MONITOR.base       import app
    from ULT_FRIDGE6_MONITOR.theme      import images
    from ULT_FRIDGE6_MONITOR.display    import display

    # derive a new class from app
    class myapp(app):

        # setup app using Start()
        def Start(self):
            
            # instanciate image library
            self.library = images()
            # load background bitmaps
            # (all of the images in 'bkgd')
            self.library.load('bkgd')
            # load led bitmaps (blue and red only)
            self.library.load('leds', ['red', 'blue'])
            
            # use background bitmap
            # (only one image image definition in 'bkdg')
            self.Panel.BackgroundBitmap = self.library.select('bkgd')

            # led 1
            self.led1 = display(
                self.Panel,
                self.library.select('leds', 'red', ['off', 'on']),
                ['off', 'on'])
            self.led1.SetPosition((100, 100))
            
            # led 2
            self.led2 = display(
                self.Panel,
                self.library.select('leds', 'blue', ['off', 'on']),
                ['off', 'on'])
            self.led2.SetPosition((130, 100))

            self.led1.SetValue('on')
            self.led2.SetValue(1)

            # done
            return
    
    # instantiate app
    m = myapp()

    # run app
    m.Run()

    # done
    _log.print(" . end test leds")

#####################################################################
#                                                                push

if _test.flag('push'):
    pass

    # _log.print(" . start test leds")

    # from ULT_FRIDGE6_MONITOR.base       import app
    # from ULT_FRIDGE6_MONITOR.theme      import images
    # from ULT_FRIDGE6_MONITOR.display    import display

    # # derive a new class from app
    # class myapp(app):

    #     # setup app using Start()
    #     def Start(self):
            
    #         # instanciate image library
    #         self.library = images()
    #         # load background bitmaps (all of the images in 'bkgd')
    #         self.library.load('bkgd')
    #         # load led bitmaps (blue and red only)
    #         self.library.load('leds', ['red', 'blue'])
            
    #         # use background bitmap
    #         self.Panel.BackgroundBitmap = self.library.select('bkgd')

    #         # led 1
    #         self.led1 = display(
    #             self.Panel,
    #             self.library.select('leds', 'red', ['off', 'on']),
    #             ['off', 'on'])
    #         self.led1.SetPosition((100, 100))
            
    #         # led 2
    #         self.led2 = display(
    #             self.Panel,
    #             self.library.select('leds', 'blue', ['off', 'on']),
    #             ['off', 'on'])
    #         self.led2.SetPosition((130, 100))

    #         # self.led1.SetValue('on')
    #         # self.led2.SetValue(1)

    #         # done
    #         return
    
    # # instantiate app
    # m = myapp()

    # # run app
    # m.Run()

    # # done
    # _log.print(" . end test leds")

# from ULT_FRIDGE6_MONITOR.display    import push

# def push_handler(self, event):
#     _log.print(f'push pressed...')
#     return

# # load push button
# library.load('push', 'blank')
# # push 1
# push1 = push(
#     self.Panel,
#     library.select(
#         'push',
#         ['released', 'pressed'],
#         ),
#     )
# push1.SetPosition((160, 100))
# push1.BindEvent(self.push_handler)                    
