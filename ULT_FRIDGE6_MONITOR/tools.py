# file: tools.py
# content: debug and logging tools
# created: 2025 April 17
# modified: 2025 April 30
# author: Roch Schanen
# repository: https://github.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

#####################################################################
#                                                         debug_class

class debug_class():

    def __init__(self, *flags):
        self.flags = [f.upper() for f in flags]
        return

    def flag(self, *flags):
        if "NONE" in self.flags: return False
        if "ALL" in self.flags: return True
        for f in flags:
            if f.upper() in self.flags:
                return True
        if flags: return False
        return True

#####################################################################
#                                                           log_class

class log_class():

    def __init__(self, filepath = ""):
        # open log file
        self.file_handle = open(filepath, "w") if filepath else None
        # done
        return

    def __del__(self):
        # close log file
        if self.file_handle:
            self.file_handle.close()
        # done
        return

    def print(self, *args, **kwargs):
        print(*args, **kwargs)
        if self.file_handle is None: return
        kwargs["file"] = self.file_handle
        print(*args, **kwargs)
        return

    def file_header(self):
        # imports
        from os.path import realpath
        from sys import argv
        # get main file content
        fp = realpath(argv[0])  # get file path
        fh = open(fp, 'r')      # get file handle
        ft = fh.read()          # get file text
        fh.close()              # done with file
        # display header
        self.print(f" . File header is:")
        # print every lines that begins with '#'. Break
        # at the first line that doesn't start with '#'
        L = ft.split('\n')
        for l in L:
            if not l: break
            if not l[0]=="#": break
            self.print(f"   {l}")
        # done
        return

    def os_version(self):
        # imports
        from platform import system as _OS
        # diplay operating system
        self.print(f" . Operating system is {_OS()}")
        # done
        return

    def python_version(self):
        # imports
        from sys import version
        # display python version
        self.print(
            f" . Running Python version {version.split(' ')[0]}")
        # done
        return

#####################################################################
#                                                          path_class

class path_class():

    def __init__(self):
        # imports
        from sys import path as _sysPath
        # default paths
        self.paths = [
            f'{_sysPath[0]}/resources',
            f'{_sysPath[0]}',
            ]
        # done
        return

    def find(self, path):
        from os.path import isfile  as _ospathIsfile
        if _ospathIsfile(path): return path
        filepath = None
        for p in self.paths:
            fp = f"{p}/{path}"
            if _ospathIsfile(fp):
                filepath = fp
        # done
        return filepath

#####################################################################

_LOG_FILE = f".logs/tools.py.log"

_DEBUG_FLAGS = [
    'NONE',
    # 'ALL',
    # 'VERBOSE',
    # 'LOG',
    ]

_debug = debug_class(*_DEBUG_FLAGS)
_log = log_class(_LOG_FILE if _debug.flag('LOG') else "")
