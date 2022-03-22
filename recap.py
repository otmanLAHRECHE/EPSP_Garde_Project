import os

from PyQt5 import QtWidgets, uic

basedir = os.path.dirname(__file__)


class RecapUi(QtWidgets.QMainWindow):
    def __init__(self, month, year, service):
        super(RecapUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'recap.ui'), self)

        self.month = month
        self.year = year
        self.service = service

        self.setWindowTitle("RECAP Service " + self.service)

        self.title = self.findChild(QtWidgets.QLabel, "label")
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.chef = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.save = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.export = self.findChild(QtWidgets.QPushButton, "pushButton_2")

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

        self.title.setText("RECAP Service de " + self.service + " mois " + str(m) + "/" + str(self.year) + ":")







