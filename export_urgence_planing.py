import datetime
import sqlite3
import time
from calendar import monthrange

from PyQt5.QtWidgets import QFileDialog, QMessageBox

import urgence

from PyQt5 import QtWidgets, uic

from threads import ThreadGuard
from tools import create_garde_page
import os

basedir = os.path.dirname(__file__)

class ExportUrgencePlaningUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(ExportUrgencePlaningUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'export_planing.ui'), self)

        self.month = month
        self.year = year

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

        self.ttl.setText("Exporté le planing de garde service d urgence " + m + "/" + str(self.year))

        self.thr = ThreadGuard(self.num_days, self.month, self.year)
        self.thr._signal.connect(self.signal_accept)
        self.thr._signal_result.connect(self.signal_accept)
        self.thr.start()

    def export_pdf(self):
        print(self.data)
        filePath, _ = QFileDialog.getSaveFileName(self, "Save garde", "",
                                                  "PDF(*.pdf);;All Files(*.*) ")

        # if file path is blank return back
        if filePath == "":
            message = "destination untrouvable"
            self.alert_(message)
        else:
            create_garde_page("URGENCE", "GARDE MEDECINS GENERALISTE", self.month, self.year, self.data, filePath)
            self.next_page = urgence.UrgenceMainUi()
            self.next_page.show()
            print(self.thr.isFinished())
            self.close()

    def signal_accept(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        elif type(progress) == list:
            self.progress.setValue(100)
            self.data = progress
            print(self.data)
            self.status.setText("complete, click sur exporter")
            self.export.setEnabled(True)

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()









