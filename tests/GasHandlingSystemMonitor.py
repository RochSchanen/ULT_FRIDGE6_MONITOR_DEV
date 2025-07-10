# file: LeakDetector_Monitor_AnalogOutput.py
# create: 2024 03 25
# author: Roch Schanen

from sys import exit
from time import strftime
from time import localtime
from time import monotonic
# from time import sleep
from time import perf_counter
from socket import gethostname
# from os.path import exists


#####################################################################
#                                                               DEBUG

_DEBUG = [
    # "ALL",
    # VERBOSE,
    # "NONE",
    "TEMPFILE",
    "SINGLE",
    "LOG",
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
    "LU-CZC2098L9S": {

        "DEVICENAME": "Dev1",

        # "REMOTEFILEPATH": None,

        "LOCALFILEPATH": '.',
        "SAVINGINTERVALS": 0.2,

        "TEMPFILEPATH": '.',
        "TEMPFILENAME": 'tmp.dat',
    },

}[gethostname().upper()]


#####################################################################
#                                                               SETUP

dn = configuration["DEVICENAME"]

lfp = configuration["LOCALFILEPATH"]
tfp = configuration["TEMPFILEPATH"]

dt = 0.20  # time intervals [s]


#####################################################################
#                                                               FILES

class monitor_file():

    def __init__(self, fp, fn):
        #  new file path (time stamped)
        fp = fp.rstrip('/')
        ts = strftime(r'%Y%m%dT%H%M%S', localtime())
        self.fp = f"{fp}/{fn}{ts}.dat"
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
        # setup saving timer (flush data every 'SAVINGINTERVALS')
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
            self.headertext += f"{l[n:]}\n"
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


# instanciate file
fh = monitor_file(lfp, "GHS_monitor_local_data_")

fh.writeheaderblock(f"""
file.local   :  {lfp.split('/')[-1]}
intervals    :  {dt}s
column 1     :  time stamp [HH:MM:SS.F]
column 2     :  seconds [s]
column 3     :  leak rate [mbar.l/s]
""")

# file.remote  :  {rfp.split('/')[-1]}


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
        return f"{astr}, {dstr}"


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

# fh.writedata("")
# fh.flushdata()

# #####################################################################

# from datetime import datetime
# from time import sleep, time
#                                                                # LOOP
# def RunningThread():

#     if _debug("showdata"):
#         i = 0 # init var

#     ii, W = 0, []

#     while Running:

#         if _debug("showdata"):
#             print(f"COUNT #{i:02} ")

#         ########## DELAY

#         sleep(dt)

#         ########## RETRIEVE

#         # get time stamp
#         ts = datetime.now().strftime('%H:%M:%S.%f')

#         # get decade, mantisse
#         d, m = u.Read()

#         if _debug("showdata"):
#             print("ts, d, m = ", ts, d, m)

#         ########## ANALYSE

#         # get time in seconds from the begining of the day
#         # H, M, S = ts.split(":")
#         # s = int(H)*3600 + int(M)*60 + float(S)
#         s = time()

#         # COMPUTE LEAK RATE FROM MANTISSE AND DECADE VOLTAGES
#         # "RECORDER mode" must be "LR"
#         # (menu 13 on leak detector UL200+)
#         # The manual can be found at:
#         # \\luna\FST\PY\Milikelvin\...
#         # ...Manuals_MagnetsAndDevices_calibrations\...
#         # ...LeakDetector_Leybold_ul-200.pdf
#         lr = m*10**(int(2*d-2.0+0.5)-12)

#         ########## RECORD

#         # record data
#         w = f"{ts[:-5]}\t{s:12.1f}\t{lr:8.3e}\n"

#         if _debug("showdata"): print(w)

#         W.append(w)
#         ii += 1

#         # write list to file
#         if ii>=5:
#             # write and flush
#             fh = open(flfp, 'a')
#             while W:
#                 w = W.pop(0)
#                 fh.write(w)
#             fh.flush()
#             fh.close()
#             ii = 0

#         ########## END

#         if _debug("showdata"):
#             i += 1

#     # done (thread ends here)
#     return

# ########## INSTANCIATE DEVICES

# u = USB6008()

# ########## SETUP FILES

# # open file
# fh = open(flfp, 'w')

# # flush header
# flushheader(fh)

# fh.close()

# ########## SETUP DEVICES

# u.Open()
# u.Configure()
# u.Start()

# ########## MAIN LOOP (THREAD)

# from threading import Thread as thread

# # create/configure thread
# LOOP = thread(target = RunningThread)

# # setup environment
# Running = True

# # start
# LOOP.start()

# # get any user input (press ENTER to interrupt)
# i = input()
# print("--- INTERRUPTING ---")

# # clear running flag -> signal thread to interrupt
# Running = False

# # wait for LOOP to complete
# LOOP.join()

# ########## CLOSE/RELEASE DEVICES

# u.Stop()
# u.Close()

# ########## CLOSE/RELEASE FILES

# fh.close()

# ########## EXIT

# exit()
