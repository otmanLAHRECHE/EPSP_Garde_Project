import os
from calendar import monthrange

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import urgence_inf
from threads import ThreadGuardUrgenceInf
from tools import create_garde_page, create_garde_inf_page

basedir = os.path.dirname(__file__)


class ExportUrgenceInf(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(ExportUrgenceInf, self).__init__()
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

        self.ttl.setText("Exporté le planing de garde d urgence (Infirmiers)" + m + "/" + str(self.year))

        self.thr = ThreadGuardUrgenceInf(self.num_days, self.month, self.year)
        self.thr._signal.connect(self.signal_accept)
        self.thr._signal_result.connect(self.signal_accept)
        self.thr._signal_finish.connect(self.signal_accept)
        self.thr._signal_groupes.connect(self.signal_accept_groupes)

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
            create_garde_inf_page("URGENCE", "GARDE (GROUPE DES INFIRMIERS)", self.month, self.year, self.data, self.groupes, filePath)
            self.next_page = urgence_inf.UrgenceInfUi()
            self.next_page.show()
            print(self.thr.isFinished())
            self.close()

    def signal_accept(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        elif type(progress) == list:
            self.data = progress
            print(self.data)
        elif type(progress) == bool:
            self.progress.setValue(100)
            self.status.setText("complete, click sur exporter")
            self.export.setEnabled(True)


    def signal_accept_groupes(self, progress):
        if type(progress) == list:
            self.groupes = progress

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()