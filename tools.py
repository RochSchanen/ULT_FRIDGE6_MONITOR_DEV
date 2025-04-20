# file: tools.py
# content: coding tools
# created: 2025 April 17
# modified: 2025 April 17
# author: Roch Schanen
# repository:
# comment:

"""    --- motivation ---

    A tool box library to help with code debugging, logging, etc.
    - The debug class to help managing flags.
    - The log class to display and log messages.

"""

class debug_class():

    def __init__(self, *flags):
        self.flags = [f.upper() for f in flags]
        return

    def flag(self, *flags):
        if "NONE" in self.flags:
            return False
        if "ALL" in self.flags:
            return True
        for f in flags:
            if f.upper() in self.flags:
                return True
        if flags:
            return False
        return True

class log_class():

    def print(self, *args, **kwargs):
        print(*args, **kwargs)
        if not self.file_handle: return
        kwargs["file"] = self.file_handle
        print(*args, **kwargs)
        return

    def _boxprint_linux(self, s):
        n = len(s)+2
        self.print()
        self.print(f"┌{'─'*n}┐")
        self.print(f"│ { s } │")
        self.print(f"└{'─'*n}┘")
        self.print()
        return

    def _boxprint_default(self, s):
        n = len(s)+2
        self.print()
        self.print(f":{'-'*n}:")
        self.print(f": { s } :")
        self.print(f":{'-'*n}:")
        self.print()
        return

    def __init__(self, filepath):
        from platform import system as _OS
        _CONFIG = {
            'Linux'  : {'boxprint': self._boxprint_linux},
            'Darwin' : {'boxprint': self._boxprint_default},
            'Windows': {'boxprint': self._boxprint_default},

        }[_OS()]
        self.boxprint = _CONFIG['boxprint']
        self.file_handle = open(filepath, "w")
        return

    def display_file_header(self):
        from os.path import realpath
        from sys import argv
        # get main script content
        fp = realpath(argv[0])                  # file path
        fh = open(fp, 'r', encoding='utf-8')    # file handle
        ft = fh.read()                          # file text
        fh.close()                              # done
        # display title
        self.boxprint(f"file header")
        # print every lines while they begin with #
        L = ft.split('\n')
        for l in L:
            if not l: break
            if not l[0]=="#": break
            self.print(l)
        # done
        return

    def display_os_version(self):
        from platform import system as _OS
        self.boxprint(f"operating system")
        self.print(f"OS is {_OS()}")
        return

    def display_python_version(self):
        from sys import version
        self.boxprint(f"python version")
        self.print(f"run Python version {version.split(' ')[0]}")
        return

    def display_version_history(self, history):
        version = list(history.keys())[-1]
        self.boxprint(f"code version")
        self.print(f"code version is '{version}'")
        self.boxprint(f"versions history")
        for v in history.values():
            self.print(v)
        return version
