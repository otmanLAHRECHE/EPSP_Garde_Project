import os
from calendar import monthrange

from PyQt5 import QtWidgets, uic
basedir = os.path.dirname(__file__)

class ExportRecapUi(QtWidgets.QMainWindow):
    def __init__(self, month, year, service):
        super(ExportRecapUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'export_planing.ui'), self)

        self.month = month
        self.year = year
        self.service = service

        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.progress.setValue(0)
        self.status = self.findChild(QtWidgets.QLabel, "label_2")
        self.export = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.export.setEnabled(False)
        self.export.clicked.connect(self.export_pdf)
        self.status.setText("Preparation des données")
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

        self.ttl.setText("Exporté le RECAP service du" + self.service + " mois de  " + m + "/" + str(self.year))


