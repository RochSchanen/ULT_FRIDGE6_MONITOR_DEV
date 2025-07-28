# file: LeakDetector_Monitor_AnalogOutput.py
# create: 2024 03 25
# author: Roch Schanen

from sys import exit
from time import time
from time import strftime
from time import localtime
from time import monotonic
from time import sleep
from time import perf_counter
from datetime import datetime
from socket import gethostname
from threading import Thread

# from os.path import exists

VERSION = "0.00"

#####################################################################
#                                                               DEBUG

_DEBUG = [
    # "ALL",
    # VERBOSE,
    # "NONE",
    # "TEMPFILE",
    # "SHOWDATA",
    # "SINGLE",
]


def _debug(*flags):
    if "NONE" in _DEBUG: return False
    if "ALL" in _DEBUG: return True
    for f in flags:
        if f.upper() in _DEBUG: return True
    if flags: return False
    return True


# def checkpath(fp):
#     if not fp[-1] == '/': fp += '/'
#     if not exists(fp): exit(f"path '{fp}' not found.")
#     if _debug(): print(f"path '{fp}' checked.")
#     # done
#     return True


#####################################################################
#                                                                HOST

if _debug(): print(f"identified hostname '{gethostname()}'")


#####################################################################
#                                                              CONFIG
configuration = {

    # "LU-CZC2098L9S": {

    "LU-S4KT4696": {

        "DEVICENAME": "Dev1",

        "FILEPATH": "//luna/FST/PY/Milikelvin/fridge_6/0.MEASUREMENTS/RUN2025-0",

        "LOCALFILEPATH": '.',
        "SAVINGINTERVALS": 5.0,

        "TEMPFILEPATH": '.',
        "TEMPFILENAME": 'tmp.dat',
    },

}[gethostname().upper()]


#####################################################################
#                                                               SETUP

setup = {
    "MESUREMENTINTERVAL": 1,  # [S]
}

dn = configuration["DEVICENAME"]
lfp = configuration["FILEPATH"]
tfp = configuration["TEMPFILEPATH"]


#####################################################################
#                                                               FILES

class monitor_file():

    def __init__(self, fp, fn):
        # record time stamp
        self.created = strftime(r'%Y%m%dT%H%M%S', localtime())
        #  new file path (time stamped)
        fp = fp.rstrip('/')
        self.fp = f"{fp}/{fn}{self.created}.dat"
        # force fixed temporary file name for debugging
        if _debug("TEMPFILE"):
            fp = configuration['TEMPFILEPATH']
            fn = configuration['TEMPFILENAME']
            self.fp = f"{fp}/{fn}"
            # clear file
            fh = open(self.fp, "w")
            fh.close()
        # declare header text and data list
        self.headertext, self.data = "", []
        # setup timer
        self.time = monotonic() + configuration['SAVINGINTERVALS']
        # done
        return

    def flushheader(self, fh):
        fh.write(self.headertext)
        self.headertext = None
        return

    def writeheaderblock(self, b):
        for i, l in enumerate(b.split(f"\n")[1:-1]):
            if i == 0: n = len(l) - len(l.lstrip())
            self.headertext += f"# {l[n:]}\n"
        return

    def savedata(self):
        if not self.data: return
        if monotonic() < self.time: return
        fh = open(self.fp, "a")
        if self.headertext: self.flushheader(fh)
        for d in self.data: fh.write(f"{d}\n")
        fh.close()
        self.data = []
        # reset timer
        self.time = monotonic() + configuration['SAVINGINTERVALS']
        # done
        return

    def writedata(self, datastr):
        # append line of data
        self.data.append(datastr)
        # try saving available data
        self.savedata()
        # done
        return

    def flushdata(self):
        self.time = monotonic()
        self.savedata()
        # done
        return


#####################################################################
#                                                         NI USB-6008

class USB6008():

    def __init__(self):

        self.ah = None  # Analogue Handle
        self.dh = None  # Digital Handle

        # --- check for devices availability
        # if not device in list:
        #     print(f"failed to find instrument {device}.")
        #     exit()

        return

    def Open(self):
        # --- should open one of the available device
        # see comments above on device availability
        from nidaqmx import Task
        # one task for each channel
        self.ah = Task()
        self.dh = Task()
        # done
        return

    def Close(self):
        # close Analogue channels
        self.ah.close()
        self.ah = None
        # close Digital channels
        self.dh.close()
        self.dh = None
        return

    def Configure(self):

        from nidaqmx.constants import TerminalConfiguration
        from nidaqmx.constants import VoltageUnits
        from nidaqmx.constants import LineGrouping

        # analogue input channels
        self.ah.ai_channels.add_ai_voltage_chan(
            f"{configuration['DEVICENAME']}/ai0:7",
            min_val=0.0,
            max_val=10.0,
            terminal_config=TerminalConfiguration.RSE,  # RSE/DIFF
            units=VoltageUnits.VOLTS,
        )

        # digital input channels
        self.dh.di_channels.add_di_chan(
            f"{configuration['DEVICENAME']}/port0/line0:7",
            line_grouping=LineGrouping.CHAN_PER_LINE,
        )

        # done
        return

    def Start(self):
        self.ah.start()
        self.dh.start()
        return

    def Stop(self):
        self.ah.stop()
        self.dh.stop()
        return

    def Read(self):
        astr = self.ah.read()
        dstr = self.dh.read()
        # return data
        return astr + dstr


#####################################################################
#                                                         NI USB-6008

if _debug("single"):

    u = USB6008()
    u.Open()
    u.Configure()
    u.Start()

    # measure delays
    time_start = perf_counter()

    data = u.Read()

    # measure delays and display
    time_delay = perf_counter() - time_start
    print(data, f": measured in {time_delay*1000:.3f}ms")

    # clean up
    u.Stop()
    u.Close()

    exit()


# #####################################################################
#                                                                  LOOP

def RunningThread():

    if _debug("SHOWDATA"): i = 0  # init var

    while Running:

        if _debug("SHOWDATA"): print(f"COUNT #{i:02} ")

        # -------------------- MEASUREMENTS INTERVAL --------------------

        sleep(setup['MESUREMENTINTERVAL'])

        # -------------------- RETRIEVE MEASUREMENTS --------------------

        # get time stamp
        ts = datetime.now().strftime('%H:%M:%S.%f')

        # get pressures and warnings
        data = u.Read()
        P_ST, P_RB, P_RS, P_AI, P_AO, P_TR, P_CD, P_PT = data[:8]
        F_BP, F_BT, F_SP, F_ST, F_AI, F_AO, F_OS, F_OP = data[8:]

        if _debug("SHOWDATA"): print(data)

        # -------------------- ANALYSE --------------------
        s = time()
        # compute pressure values, flow rate, ...

        # -------------------- RECORD --------------------

        # record data
        w = f"{ts[:-5]}\t"
        w += f"{s:12.1f}\t"
        w += f"{P_ST:8.3e}\t"
        w += f"{P_RB:8.3e}\t"
        w += f"{P_RS:8.3e}\t"
        w += f"{P_AI:8.3e}\t"
        w += f"{P_AO:8.3e}\t"
        w += f"{P_TR:8.3e}\t"
        w += f"{P_CD:8.3e}\t"
        w += f"{P_PT:8.3e}\t"
        w += f"{['ON', 'OFF'][F_BP]}\t"
        w += f"{['ON', 'OFF'][F_BT]}\t"
        w += f"{['ON', 'OFF'][F_SP]}\t"
        w += f"{['ON', 'OFF'][F_ST]}\t"
        w += f"{['ON', 'OFF'][F_AI]}\t"
        w += f"{['ON', 'OFF'][F_AO]}\t"
        w += f"{['ON', 'OFF'][F_OS]}\t"
        w += f"{['ON', 'OFF'][F_OP]}"

        if _debug("SHOWDATA"):
            print(w)
            i += 1

        fh.writedata(w)

    # finalise thread
    fh.flushdata()
    # done (thread ends here)
    return


# INSTANCIATE DEVICES

u = USB6008()

# SETUP FILES

fh = monitor_file(configuration['FILEPATH'], "GHS_")
fh.writeheaderblock(f"""
file      : {fh.fp.split('/')[-1]}
content   : "Gas Handling System" raw data
created   : {fh.created}
author    : GasHandlingSystemMonitor.py V{VERSION}
column 01 : time stamp [HH:MM:SS.F]
column 02 : time in seconds [s]
column 03 : still pressure [bar] wrong -> this is the general thermovac display
column 04 : big roots outlet pressure [bar]
column 05 : small roots outlet pressure [bar]
column 06 : ACP40 inlet [bar]
column 07 : ACP40 outlet [bar]
column 08 : pressure before traps [bar]
column 09 : pressure after traps [bar] (condensing pressure)
column 10 : 1K pot pressure [bar]
column 11 : big roots high pressure warning
column 12 : big roots high temperature warning
column 13 : small roots high pressure warning
column 14 : small roots high temperature warning
column 15 : ACP40 inlet high pressure warning
column 16 : ACP40 outlet high pressure warning
column 17 : Override switch activated
column 18 : Override plug inserted
""")

# SETUP DEVICES

u.Open()
u.Configure()
u.Start()

# SETUP LOOP (THREAD)

LOOP = Thread(target=RunningThread)
Running = True
LOOP.start()

# run until user press enter
i = input()
print("--- INTERRUPTING ---")
Running = False

# FINALISING

LOOP.join()
u.Stop()
u.Close()
fh.flushdata()
exit()
