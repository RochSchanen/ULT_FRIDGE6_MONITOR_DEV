# file: logbook.py
# content: log function
# created: 2025 June 02 Monday
# author: Roch Schanen

# include a config file (local? remote?)


_fh = open("./log.txt", 'w')


def lprint(*args, **kwargs):
    print(*args, **kwargs)
    kwargs["file"] = _fh
    return print(*args, **kwargs)
