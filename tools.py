# file: tools.py
# content: debug and logging tools
# created: 2025 April 17
# modified: 2025 April 22
# author: Roch Schanen
# repository: https://github.com/RochSchanen/ULT_FRIDGE6_MONITOR_DEV

#####################################################################
#                                                     ### DESCRIPTION
#
_DESCRIPTION = """   
 
    --- motivation ---

    This is a minimal library to help with
    debugging scripts and logging messages.

"""

#####################################################################
#                                                         ### HISTORY
# The only available versions is "0.00"
#
_HISTORY = {

    "0.00": """
        Add 'debug_class' and 'log_class':
    
            . 'debug_class.__init__(*flags)' sets the flags during
            instantiation (by passing the names of the flags as
            strings). There is two reserved flags: 1) The flag 'NONE'
            which clears all flags and has precedence over all the
            other flags. 2) The flag 'ALL' which sets all flags (all
            flags are selected except the flag 'NONE').

            . 'debug_class.flag(*flags)' tests if any of the flags
            parameters (passed as strings) is set.

            . 'log_class.__init__(filepath = "")' defines the log
            file for logging messages during instantiation. If the
            'filepath' parameter is left empty (default value), no
            file is created, and the 'log_class.print()' method
            writes only to the standard output. If 'filepath' is
            defined, the 'log_class.print()' method write both to
            the standard output and to the log file.

            . use 'log_class.print(*args, **kwargs)' exactly as you
            would use the standard 'print(*args, **kwargs)' function.

            . use 'log_class.boxprint(s)' to print a string 's' that
            is surrounded by a decorating box to emphasize the text.
            The style of the box depends on the operating system.
            The reason is that some python versions cannot display
            some Unicode characters.

            . Some additional methods are useful to display some
            complementary information when running the python code:

            . use 'log_class.file_header()' to log the header of the
            main script. The header correspond to all the line at the
            beginning of the file that start with the hash sign.

            . use 'log_class.os_version()' to log the current version
            of operating system.
            
            . use 'log_class.python_version()' to log the current
            python version used to run the code.
            
            . use 'log_class.history()' to log the file history.
            This text is part of the file history.
    """,
}

#####################################################################
#                                                         ### LIBRARY
#
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

class log_class():

    def print(self, *args, **kwargs):
        print(*args, **kwargs)
        if self.file_handle is None: return
        kwargs["file"] = self.file_handle
        print(*args, **kwargs)
        return

    # decorated messages

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
        self.print(f"#{'#'*n}#")
        self.print(f"# { s } #")
        self.print(f"#{'#'*n}#")
        self.print()
        return

    def __init__(self, filepath = ""):

        # os dependent configuration
        from platform import system as _OS
        _CONFIG = {
            'Linux'  : {'boxprint': self._boxprint_linux},
            'Darwin' : {'boxprint': self._boxprint_default},
            'Windows': {'boxprint': self._boxprint_default},

        }[_OS()]
        
        # os dependent setup
        self.boxprint = _CONFIG['boxprint']
        
        # file setup
        self.file_handle = open(filepath, "w") if filepath else None
        
        # done
        return

    def file_header(self):

        from os.path import realpath
        from sys import argv

        # get main file content
        fp = realpath(argv[0])                  # get file path
        fh = open(fp, 'r', encoding='utf-8')    # get file handle
        ft = fh.read()                          # get file text
        fh.close()                              # done with file

        self.print(f" . File header is:")

        # print every lines that begins with '#'. Stop
        # at the first line that doesn't start with '#'
        L = ft.split('\n')
        for l in L:
            if not l: break
            if not l[0]=="#": break
            self.print(f"   {l}")

        # done
        return

    def os_version(self):
        from platform import system as _OS
        self.print(f" . Operating system is {_OS()}")
        # done
        return

    def python_version(self):
        from sys import version
        self.print(
            f" . Running Python version {version.split(' ')[0]}")
        # done
        return

    def history(self, history):
        self.print(f" . file history is:")
        for k in sorted(history):
            self.print(f"    . version {k}:")
            self.print(history[k])
        self.print(f" . Last file version is '{k}'")
        # done
        return

#####################################################################
#                                                           ### DEBUG
# uncomment line to set any flag:
#
# . NONE    : clears all flags (precedes the 'ALL' flag)
# . ALL     : sets all flags (all flags are selected except 'NONE')
# . LOG     : log messages to file
# . VERBOSE : display extra informations
# . TEST    : enable the selected tests
#
_debug = debug_class(
    # 'ALL',
    # 'NONE',
    'VERBOSE',  # only performed when __main__
    'TESTS',    # only performed when __main__
    'LOG',
    )

#####################################################################
#                                                             ### LOG
# The default log file is 'tools.py.log'
# Use the debugging 'LOG' flag to activate messages logging.
#
_log = log_class("./tools.py.log" if _debug.flag('LOG') else "")

#####################################################################
#                                                            ### TEST
#
if _debug.flag('TESTS'):
    _test = debug_class(
        sorted(_HISTORY)[-1],   # run last version
        # "X.XX",               # run version X.XX
        )

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

        if _test.flag('X.XX'):
            _log.print(" . running test for version X.XX")

_log.boxprint('done')
