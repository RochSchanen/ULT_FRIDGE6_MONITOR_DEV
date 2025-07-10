# file: ultlib_nidaqmx.py
# create: 2024 03 25
# author: Roch Schanen

_DEBUG = [
    # flags must be upper case:
    # "ALL",
    "VERSION",  # display DAQmx version
    "DEVICES",  # display available devices
]

#####################################################################
#                                                               DEBUG


def _debug(*flags):
    if "NONE" in _DEBUG: return False
    if "ALL" in _DEBUG: return True
    for f in flags:
        if f.upper() in _DEBUG: return True
    if flags: return False
    return True


#####################################################################

import nidaqmx as _DAQ

# from _DAQ.constants import TerminalConfiguration
# from _DAQ.nidaqmx.constants import VoltageUnits

_l = _DAQ.system.System.local()

# print(_DAQ.system.System.devices.device_names)

if _debug("VERSION"):
    # versions: major, minor, update
    m, n, u = _l.driver_version
    print(f"DAQmx version {m}.{n}.{u}")

# build here an "easy to use" device list.

DEVICE_LIST = {}

for d in _l.devices:

    if _debug("DEVICES"):
        print()
        print(f"DEVICES:")
        print(f"-------\n")
        print(
            f"name = '{d.name}':\n"
            + f"\tproduct_category = '{d.product_category}',\n"
            + f"\tproduct_type = '{d.product_type}',\n"
            + f"\tproduct number = '{d.product_num}',\n"
            + f"\tserial number = '{d.serial_num:08X}'.\n"
        )

    # add device to dico
