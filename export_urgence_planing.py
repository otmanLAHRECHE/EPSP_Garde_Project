from calendar import monthrange

from PyQt5 import QtWidgets, uic


class ExportUrgencePlaningUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(ExportUrgencePlaningUi, self).__init__()
        uic.loadUi('ui/export_planing.ui', self)

        self.month = month
        self.year = year

        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.status = self.findChild(QtWidgets.QLabel, "label_2")
        self.export = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.data = {}
        self.num_days = monthrange(self.year, self.month)[1]

        if self.month == 1:
            m = "janvier"
        elif self.month == 2:
            m = "février"
        elif self.month == 3:
            m = "mars"
        elif self.month == 4:
            m = "avril"
        elif self.month == 5:
            m = "mai"
        elif self.month == 6:
            m = "juin"
        elif self.month == 7:
            m = "juillet"
        elif self.month == 8:
            m = "août"
        elif self.month == 9:
            m = "septembre"
        elif self.month == 10:
            m = "octobre"
        elif self.month == 11:
            m = "novembre"
        elif self.month == 12:
            m = "décembre"





