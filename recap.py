import datetime
import os

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem

import dentiste
import infirmier
import laboratoire
import radiologie
import urgence
from dialogs import Saving_progress_dialog, CustomDialog
from threads import Thread_recap_load

basedir = os.path.dirname(__file__)


class RecapUi(QtWidgets.QMainWindow):
    def __init__(self, month, year, service):
        super(RecapUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'recap.ui'), self)

        self.month = month
        self.year = year
        self.service = service

        self.want_to_close = False

        self.setWindowTitle("RECAP Service " + self.service)

        self.title = self.findChild(QtWidgets.QLabel, "label")
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.table.hideColumn(0)
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
        self.load_recap()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "Votre liste de RECAP na pas sauvgarder, es-tu sûr de quiter"
        dialog = CustomDialog(message)
        if not self.want_to_close:
            if dialog.exec():
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
                    self.next_page = dentiste.DentisteMainUi()
                elif self.service == "urgence_surv":
                    self.next_page = dentiste.DentisteMainUi()
                elif self.service == "urgence_inf":
                    self.next_page = dentiste.DentisteMainUi()

                self.next_page.show()
                self.close()
            else:
                a0.ignore()
        else:
            self.close()

    def load_recap(self):
        self.dialog = Saving_progress_dialog()
        self.dialog.label.setText("loading RECAP")
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.thr1 = Thread_recap_load(self.month, self.year, self.service)
        self.thr1._signal.connect(self.signal_accepted_load)
        self.thr1._signal_status.connect(self.signal_accepted_load)
        self.thr1._signal_finish.connect(self.signal_accepted_load)
        self.thr1._signal_users.connect(self.signal_accepted_load_users)
        self.thr1.start()

    def signal_accepted_load(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:

            agents_name = progress[0]
            jo = progress[1]
            jw = progress[2]
            jf = progress[3]
            pr = progress[4]

            self.table.setRowHeight(pr, 50)
            self.table.setItem(pr, 1, QTableWidgetItem(agents_name))
            self.table.setItem(pr, 2, QTableWidgetItem(str(jo)))
            self.table.setItem(pr, 3, QTableWidgetItem(str(jw)))
            self.table.setItem(pr, 4, QTableWidgetItem(str(jf)))
            total = jo + jw + jf
            self.table.setItem(pr, 5, QTableWidgetItem(str(total)))

        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            self.dialog.close()

    def signal_accepted_load_users(self, progress):

        self.chef.addItem("")

        for worker in progress:
            self.chef.addItem(worker[0])
