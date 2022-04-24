import datetime
import sqlite3
from calendar import monthrange

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

import export_radio_guard
import radiologie
from dialogs import Saving_progress_dialog, CustomDialog
from threads import Thread_load_guards_radio, Thread_create_radio_guard, ThreadAutoGuard
from widgets import Chose_worker
import os
basedir = os.path.dirname(__file__)

class RadiologieGuardUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(RadiologieGuardUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'guard_radio.ui'), self)

        self.want_to_close = False

        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.save = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.save.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'save.png')))

        self.exportPd = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.exportPd.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'download.png')))

        self.auto = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.auto.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'auto.png')))

        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 220)

        self.month = month
        self.year = year
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

        self.ttl.setText("Planing de garde radiologie mois " + str(m) + "/" + str(self.year) + ":")
        self.load_med()
        self.load_guards()
        self.exportPd.clicked.connect(self.export)


        self.save.clicked.connect(self.save_)
        self.auto.clicked.connect(self.auto_)

    def load_guards(self):
        self.dialog = Saving_progress_dialog()
        self.dialog.label.setText("loading gardes")
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()


        self.thr2 = Thread_load_guards_radio(self.num_days, self.month, self.year)
        self.thr2._signal.connect(self.signal_accepted_load)
        self.thr2._signal_status.connect(self.signal_accepted_load)
        self.thr2._signal_finish.connect(self.signal_accepted_load)
        self.thr2.start()

    def load_med(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = 'SELECT full_name FROM health_worker where service=?'
        cur.execute(sql_q, ('radio',))
        self.medcins = cur.fetchall()
        connection.close()

    def save_(self):
        self.want_to_close = True
        self.dialog = Saving_progress_dialog()
        self.dialog.show()
        self.thr = Thread_create_radio_guard(self.num_days, self.month, self.year, self.table)
        self.thr._signal.connect(self.signal_accepted)
        self.thr._signal_status.connect(self.signal_accepted)
        self.thr.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "Votre liste de garde na pas sauvgarder, es-tu sûr de quiter"
        dialog = CustomDialog(message)
        if not self.want_to_close:
            if dialog.exec():
                self.next_page = radiologie.RadiologieMainUi()
                self.next_page.show()
                self.close()
            else:
                a0.ignore()
        else:
            self.next_page = radiologie.RadiologieMainUi()
            self.next_page.show()
            self.close()

    def signal_accepted(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            self.dialog.close()

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

            self.table.setCellWidget(row, 2, chose_light)
            self.table.setCellWidget(row, 3, chose_night)

        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            self.dialog.close()

    def export(self):
        self.want_to_close = True
        self.next_page = export_radio_guard.ExportRadioGuard(self.month, self.year)
        self.close()
        self.next_page.show()


    def auto_(self):
        auto = []
        for i in range(16):
            check1 = self.table.cellWidget(i, 2)
            check2 = self.table.cellWidget(i, 3)
            medInd1 = check1.chose.currentIndex()
            medInd2 = check2.chose.currentIndex()
            if medInd1 != 0:
                auto.append(medInd1)
            if medInd2 != 0:
                auto.append(medInd2)


        if len(auto) == 0:
            message = "liste vide"
            self.alert_(message)
        else:
            self.dialog = Saving_progress_dialog()
            self.dialog.show()
            self.thr3 = ThreadAutoGuard(self.num_days, self.month, self.year, "radio", self.table, auto)
            self.thr3._signal.connect(self.signal_accepted_auto)
            self.thr3._signal_status.connect(self.signal_accepted_auto)
            self.thr3._signal_result.connect(self.signal_accepted_auto)
            self.thr3.start()


    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()


    def signal_accepted_auto(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:
            chose_light = Chose_worker(self.medcins)
            chose_night = Chose_worker(self.medcins)

            chose_light.chose.setCurrentIndex(progress[1])
            chose_night.chose.setCurrentIndex(progress[2])
            self.table.setCellWidget(progress[0], 2, chose_light)
            self.table.setCellWidget(progress[0], 3, chose_night)
        else:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            self.dialog.close()