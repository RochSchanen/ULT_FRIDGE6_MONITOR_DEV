# file: theme.py
# content: image collection manager
# created: 2025 April 22
# modified: 2025 April 24
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

#####################################################################
#                                                     ### DESCRIPTION
#
_DESCRIPTION = """   
    
    --- motivation ---

        This is a library to help retrieve image from a set of .png
        files and to filter and select groups of images from the
        library of images collected. These are used for background,
        buttons, switches, etc...

"""

#####################################################################
#                                                         ### HISTORY
#
_HISTORY = {

    "0.00": """
        . add images() class

    """,
}

#####################################################################
#                                                           ### DEBUG
#
from tools import debug_class
_debug = debug_class(
    # 'VERBOSE'
    'TESTS', 
    'LOG',
    )

#####################################################################
#                                                             ### LOG
#
from tools import log_class
_log = log_class("./theme.py.log" if _debug.flag('LOG') else "")

#####################################################################
#                                                            ### TEST
#
if _debug.flag('TESTS'):
    _test = debug_class(sorted(_HISTORY)[-1])

#####################################################################
#                                                         ### IMPORTS
#
# all constants, methods and classes are imported
# individually to clarify the usage of packages.
#

# # from standard packages:
# from sys        import path             as _path
# from os.path    import isfile           as _isfile

# from wxpython: https://www.wxpython.org/

# wx bitmap methods
from wx import Bitmap                   as _wxBitmap
from wx import BITMAP_TYPE_PNG          as _wxBITMAP_TYPE_PNG
from wx import Rect                     as _wxRect

#####################################################################
#                                                         ### LIBRARY
#

class images():

    def __init__(self):
        # declare
        self.imagelibrary = {}
        # done
        return

    def load(self, name, *tags):
        # load image
        bmp = wxBitmap(fpb, wxBITMAP_TYPE_PNG)
        W, H = bmp.GetSize()
        # build file path
        fpd = f'./resources/{name}.png.txt' # definition
        fpb = f'./resources/{name}.png'     # bitmap
        # build filter
        filter = set(tags)
        # add collection
        if not name in self.imagelibrary.keys():  
            self.imagelibrary[name] = {}
        # point to image collection
        imco = self.imagelibrary[name]
        # load the definition text file line by line
        with open(fpd) as fh:
            for l in fh:
                s = l.strip()
                # skip empty and comment lines
                if s.strip() == '': continue
                if s.strip()[0] == '#': continue
                # parse geometry
                geometry = tuple(int(p) for p in l.split(',')[:8])
                # parse image tags
                imagetags = tuple(p.strip() for p in l.split(',')[8:])
                # filter and update image set
                if filter.issubset(set(imagetags)):
                    # check if image is already loaded
                    # (no overloading: change this behaviour?)
                    if not imagetags in imco.keys():
                        # retrieve geometry
                        xo, yo, nx, ny, w, h, i, j = geometry
                        # compute grid size
                        P, Q = W/nx, H/ny
                        # compute clipping origin
                        x = (i-1)*P + (P-w)/2 + xo
                        y = (j-1)*Q + (Q-h)/2 + yo
                        # set clipping geometry
                        Clip = wxRect(int(x), int(y), w, h)
                        # clip and record image in the collection
                        imco[imagetags] = bm.GetSubBitmap(Clip)
        # done
        return

    def display(self):
        for n in self.imagelibrary.keys():
            for k in self.imagelibrary[n].keys():
                x, y, nx, ny, w, h, i, j = self.imagelibrary[n][k]
                _log.print(n, k, x, y, nx, ny, w, h, i, j)

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
            _log.print()            

            from base import app

            # derive a new class from app
            class myapp(app):

                def Start(self):

                    library = images()
                    library.load('leds', 'violet')
                    _log.print()
                    library.load('leds', 'blue')
                    _log.print()
                    library.load('leds', 'red')
                    _log.print()
                    library.load('leds')

                    library.display()

                    # # manually setup the background image of myapp
                    # self.Panel.BackgroundBitmap = img

                    # done
                    return
            
            m = myapp()
            m.Run()

            _log.print()            
            _log.print(" . end test for version 0.00")
            _log.print()            
