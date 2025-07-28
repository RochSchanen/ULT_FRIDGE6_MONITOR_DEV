


from filelog import lprint
from os.path import realpath
from sys import argv


def header():

    # get main script content
    fp = realpath(argv[0])  # file path
    fh = open(fp, 'r')      # file handle
    ft = fh.read()          # file text
    fh.close()              # done
    # print lines while begin with #
    lines = ft.split('\n')
    for line in lines:
        if line[:2] == "#!":
            continue
        if line.strip() == "":
            break
        if not line[0] == "#":
            break
        lprint(line)
    # show versions
    from sys import version as sys_version
    lprint(f"using Python version {sys_version.split(' ')[0]}")
    # from pyvigi import version
    lprint(f"run script SimSys.py version 0.0")
    # done
    return
