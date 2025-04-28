# file: theme.py
# content: image collection manager
# created: 2025 April 22
# modified: 2025 April 24
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

#####################################################################
#                                                     ### DESCRIPTION
_DESCRIPTION = """   
    
    --- motivation ---

        This is a library to help collect images from a set of .png
        files and to filter and select groups of images from the
        library of images thus collected. These are meant to be used
        for background, buttons, switches, etc...

"""

#####################################################################
#                                                         ### HISTORY
_HISTORY = {

    "0.00": """
        add 'images()' class:

            . images.__init__() doesn't requires any parameters.

            . images.load(name, *tags) is used to collect images
            from a .png file. Use tags parameters to select which
            images are collected from the file. The tags are
            defined in the .png.txt file that should be next to the
            .png file. Multiple loads can be performed from the
            same file. Duplicates are automatically removed.

            . images.select(name, *tags) is used to select a subset
            of images that were loaded from a .png file. Use the tags
            parameters to select and order the images. The methods
            returns the images as a list. If there only one image in
            the list, the method returns directly the image and not
            an list of one image. 

            . check test 0.00 for examples of how to load and select
            images.
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
_log = log_class("./logs/theme.py.log" if _debug.flag('LOG') else "")

#####################################################################
#                                                            ### TEST
if _debug.flag('TESTS'):
    _test = debug_class(
        sorted(_HISTORY)[-1],   # run last version
        # "X.XX",               # run version X.XX
        )

#####################################################################
#                                                         ### IMPORTS
# from wxpython: https://www.wxpython.org/
from wx import Bitmap           as _wxBitmap
from wx import BITMAP_TYPE_PNG  as _wxBITMAP_TYPE_PNG
from wx import Rect             as _wxRect

#####################################################################
#                                                         ### LIBRARY
class images():

    def __init__(self):
        # declare the library
        self.imagelibrary = {}
        # done
        return

    # join and sort two tuple together
    def _join(self, x, y):
        # force the second argument to be a tuple
        if not isinstance(y, tuple): y = tuple([y])
        return tuple(sorted([*x, *y]))

    # build filter list by distributing the last argument
    def _filterslist(self, *tags):
        # empty case: return a list containing the empty tuple
        if not tags: return [tuple()]
        # separate arguments from last one
        a, b = tags[:-1], tags[-1]
        # force the last argument to be a list
        if not isinstance(b, list): b = [b]
        # distribute items in last argument 
        return [self._join(a, t) for t in b]

    def load(self, name, *tags):
        # get path to the image
        from tools import path_class
        path = path_class()
        fp = path.find(f'{name}.png')
        # load image bitmap
        bm = _wxBitmap(fp, _wxBITMAP_TYPE_PNG)
        # get image size
        W, H = bm.GetSize()
        # declare new collection
        if not name in self.imagelibrary.keys(): 
            self.imagelibrary[name] = {}
        # create a pointer to the collection
        collection = self.imagelibrary[name]
        # loop through filters
        for _filter in self._filterslist(*tags):
            # load the definition file line by line
            with open(f'{fp}.txt') as fh:
                for l in fh:
                    # skip empty and comment lines
                    s = l.strip()
                    if s == '': continue
                    if s[0] == '#': continue
                    # parse geometry
                    img_geom = tuple(
                        int(p) for p in s.split(',')[:8])
                    # parse tags as list
                    img_tags_list = list(
                        p.strip() for p in s.split(',')[8:])
                    # convert as a sorted tuple
                    img_tags = tuple(sorted(img_tags_list))
                    # check filter set inclusion in the tags set
                    if set(_filter).issubset(set(img_tags)):
                        # only add new images
                        if not img_tags in self.imagelibrary[name].keys():
                            # retrieve geometrical parameters
                            X, Y, p, q, w, h, m, n = img_geom                
                            # compute grid size
                            P, Q = W/p, H/q
                            # compute clipping origin
                            x = (m-1)*P + (P-w)/2 + X
                            y = (n-1)*Q + (Q-h)/2 + Y
                            # build clipping rectangle
                            Clip = _wxRect(int(x), int(y), w, h)
                            # clip bitmap and record image into library
                            collection[img_tags] = bm.GetSubBitmap(Clip)
        # done
        return

    def select(self, name, *tags):
        # declare return parameter
        r = []
        # loop through filters
        for f in self._filterslist(*tags):                
            # loop through images
            for k in self.imagelibrary[name].keys():
                if set(f).issubset(set(k)):
                    r.append(self.imagelibrary[name][k])
        # done
        if len(r) == 1:
            return r[0]
        return r

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

            from wx import MemoryDC   as _wxMemoryDC
            from wx import NullBitmap as _wxNullBitmap
            from base import app

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
                    # create device context
                    dc = _wxMemoryDC()
                    
                    # select screen bitmap
                    dc.SelectObject(self.Panel.BackgroundBitmap)
                    # draw led
                    dc.DrawBitmap(library.select('leds',  'red',   'on'),  100, 100)
                    dc.DrawBitmap(library.select('leds',  'red',  'off'),  100, 120)
                    dc.DrawBitmap(library.select('leds', ('blue',  'on')), 200, 100)
                    dc.DrawBitmap(library.select('leds', ('blue', 'off')), 200, 120)
                    
                    # release screen bitmap
                    dc.SelectObject(_wxNullBitmap)
                    
                    # done
                    return
            
            m = myapp()
            m.Run()

            _log.print(" . end test for version 0.00")
