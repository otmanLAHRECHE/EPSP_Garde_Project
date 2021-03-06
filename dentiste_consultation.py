import datetime
import os
import sqlite3
from calendar import monthrange

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem

import dentiste
import export_dentiste_consultation
from dialogs import Saving_progress_dialog, CustomDialog
from threads import Thread_load_consultation_dentiste, Thread_create_dentiste_consultation
from widgets import Chose_worker
basedir = os.path.dirname(__file__)


class DentisteConsultationUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(DentisteConsultationUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'consultation_dentiste.ui'), self)


        self.want_to_close = False

        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.save = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.exportPd = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 220)

        self.month = month
        self.year = year
        self.num_days = monthrange(self.year, self.month)[1]
        self.days_of_week_end = "Samedi" + "  " + "Vendredi"

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

        self.ttl.setText("Planing de consultation dentistes mois " + str(m) + "/" + str(self.year) + ":")
        self.load_dentiste()
        self.load_consultations()

        self.exportPd.clicked.connect(self.export)
        self.save.clicked.connect(self.save_)

    def load_consultations(self):
        print("load guard list")
        self.dialog = Saving_progress_dialog()
        self.dialog.label.setText("loading consultations")
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.thr2 = Thread_load_consultation_dentiste(self.num_days, self.month, self.year)
        self.thr2._signal.connect(self.signal_accepted_load)
        self.thr2._signal_status.connect(self.signal_accepted_load)
        self.thr2._signal_finish.connect(self.signal_accepted_load)
        self.thr2.start()

    def load_dentiste(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = 'SELECT full_name FROM health_worker where service=?'
        cur.execute(sql_q, ('dentiste',))
        self.medcins = cur.fetchall()
        connection.close()

    def save_(self):
        self.want_to_close = True
        self.dialog = Saving_progress_dialog()
        self.dialog.show()
        self.thr = Thread_create_dentiste_consultation(self.num_days, self.month, self.year, self.table)
        self.thr._signal.connect(self.signal_accepted)
        self.thr._signal_status.connect(self.signal_accepted)
        self.thr.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "Votre liste de consultation na pas sauvgarder, es-tu sûr de quiter"
        dialog = CustomDialog(message)
        if not self.want_to_close:
            if dialog.exec():
                self.next_page = dentiste.DentisteMainUi()
                self.next_page.show()
                self.close()
            else:
                a0.ignore()
        else:
            self.next_page = dentiste.DentisteMainUi()
            self.next_page.show()
            self.close()

    def signal_accepted(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            print(progress)
            self.dialog.close()
            self.next_page = dentiste.DentisteMainUi()
            self.next_page.show()
            self.close()

    def signal_accepted_load(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:

            row = progress[0]
            results_light = progress[1]
            results_night = progress[2]

            day = row + 1
            x = datetime.datetime(self.year, self.month, day)
            m = ""
            if x.strftime("%A") == "Saturday":
                m = "Samedi"
            elif x.strftime("%A") == "Sunday":
                m = "Dimanche"
            elif x.strftime("%A") == "Monday":
                m = "Lundi"
            elif x.strftime("%A") == "Tuesday":
                m = "Mardi"
            elif x.strftime("%A") == "Wednesday":
                m = "Mercredi"
            elif x.strftime("%A") == "Thursday":
                m = "Jeudi"
            elif x.strftime("%A") == "Friday":
                m = "Vendredi"

            self.table.setRowHeight(row, 50)
            self.table.setItem(row, 0, QTableWidgetItem(m))
            self.table.setItem(row, 1, QTableWidgetItem(str(day) + "/" + str(self.month) + "/" + str(self.year)))
            chose_light = Chose_worker(self.medcins)
            chose_night = Chose_worker(self.medcins)

            if results_light:
                print(results_light)
                rl = results_light[0]
                chose_light.chose.setCurrentText(str(rl[0]))
            if results_night:
                print(results_night)
                rn = results_night[0]
                chose_night.chose.setCurrentText(str(rn[0]))

            if m in self.days_of_week_end:
                print("nothing")
            else:
                self.table.setCellWidget(row, 2, chose_light)
                self.table.setCellWidget(row, 3, chose_night)

        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            self.dialog.close()

    def export(self):
        self.want_to_close = True
        self.next_page = export_dentiste_consultation.ExportDentisteConsultationUi(self.month, self.year)
        self.close()
        self.next_page.show()
