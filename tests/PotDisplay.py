# file: PotDisplay.py
# create: 2025 07 18
# author: Roch Schanen

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import QTimer
from pyqtgraph import GraphicsLayoutWidget
from pyqtgraph import DateAxisItem
from pyqtgraph import LabelItem
from sys import argv


class myGraphicsLayoutWidget(GraphicsLayoutWidget):

    def __init__(self):

        # call parent constructor
        super().__init__(
            parent=None,
            show=True,
            size=(600, 600),
        )

        # timer configuration
        self.t = QTimer(self)
        self.t.setInterval(6000)
        self.t.start()
        self.t.timeout.connect(self.RefreshPlot)

        # create plot window
        self.pw = self.addPlot()
        self.pw.getViewBox().setBorder()
        self.pw.setAxisItems({'bottom': DateAxisItem(utcOffset=None)})
        self.pw.setLogMode(y=True)
        self.pw.setYRange(-1, 2)
        self.pw.showGrid(x=True, y=True)
        self.pw.setMouseEnabled(x=False, y=False)
        self.pw.hideButtons()

        self.lbl = LabelItem("", size="32pt", color="#FFFFFF")
        self.lbl.setParentItem(self.pw.graphicsItem())
        self.lbl.anchor(itemPos=(0.5, 0.5), parentPos=(0.5, 0.05))

        # create plot data
        self.pd = self.pw.plot(
            [],
            connect='all',
            symbolSize=5,
            pen="#8888FF",
            symbolPen="#8888FF",
            symbolBrush="#0000FF",
        )

        # create vertical layout
        self.vbl = QVBoxLayout()

        # apply vetical layout to main window
        self.setLayout(self.vbl)

    def RefreshPlot(self):

        fh = open(f"{fn}", 'r')
        text = fh.read()
        fh.close()

        X, Y = [], []

        for lbl in text.split("\n"):
            if lbl == "": continue
            if lbl[0] == "#": continue
            datalist = lbl.split("\t")
            X.append(float(datalist[1]))

            v = datalist[9]
            # e = (float(v) - 6.143) / 1.286
            # p = 10 ** e

            p = float(v) * 6

            Y.append(p)

        self.pd.setData(X[-bfl * 60:], Y[-bfl * 60:])
        self.lbl.setText(f"1K POT {Y[-1]:.2f} [mbar]")


def getlast(fp):
    from os import listdir
    fl = []
    for fn in listdir(fp):
        # filter file name
        if not fn[:4] == "GHS_": continue
        if not fn[-4:] == ".dat": continue
        # append to list if valid name
        fl.append(fn)
    # sort in ascending order (alphabetical)
    fl.sort()
    # return full path
    return f"{fp}/{fl[-1]}"


# get path to data
fp = '//luna/FST/PY/Milikelvin/fridge_6/0.MEASUREMENTS/RUN2025-0/'

fn = getlast(fp)
bfl = 10 if len(argv) == 1 else int(argv[1])
app = QApplication([])
glw = myGraphicsLayoutWidget()
app.exec()
