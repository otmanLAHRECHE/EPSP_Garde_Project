import os
from calendar import monthrange

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

import dentiste
import infirmier
import laboratoire
import pharmacie
import radiologie
import urgence
from tools import create_garde_page

basedir = os.path.dirname(__file__)


class ExportRecapUi(QtWidgets.QMainWindow):
    def __init__(self, month, year, service, chef):
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

    def export_pdf(self):
        print(self.data)
        """
        filePath, _ = QFileDialog.getSaveFileName(self, "Save garde", "",
                                                  "PDF(*.pdf);;All Files(*.*) ")


        if filePath == "":
            message = "destination untrouvable"
            self.alert_(message)
        else:
            create_garde_page("URGENCE", "GARDE URGENCE", self.month, self.year, self.data, filePath)

            if self.service == "urgence":
                self.next_page = urgence.UrgenceMainUi()
            elif self.service == "dentiste":
                self.next_page = dentiste.DentisteMainUi()
            elif self.service == "dentiste_inf":
                self.next_page = infirmier.InfermierMainUi()
            elif self.service == "labo":
                self.next_page = laboratoire.LaboratoireMainUi()
            elif self.service == "radio":
                self.next_page = radiologie.RadiologieMainUi()
            elif self.service == "pharm":
                self.next_page = pharmacie.PharmacieMainUi()
            elif self.service == "urgence_surv":
                self.next_page = dentiste.DentisteMainUi()
            elif self.service == "urgence_inf":
                self.next_page = dentiste.DentisteMainUi()

            self.next_page.show()
            print(self.thr.isFinished())
            self.close()
            """

    def signal_accept(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        elif type(progress) == list:
            self.progress.setValue(100)
            self.data = progress
            print(self.data)
            self.status.setText("complete, click sur exporter")
            self.export.setEnabled(True)
