# file: theme.py
# content: image collection manager
# created: 2025 April 22
# modified: 2025 April 30
# author: Roch Schanen
# repository: https://GitHub.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

_LOG_FILE = f".logs/theme.py.log"

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
#                                                              import

# from wxpython: https://www.wxpython.org/

# images
from wx import Bitmap           as _wxBitmap
from wx import BITMAP_TYPE_PNG  as _wxBITMAP_TYPE_PNG
from wx import Rect             as _wxRect

# local
from ULT_FRIDGE6_MONITOR.tools import path_class

#####################################################################
#                                                              images

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
