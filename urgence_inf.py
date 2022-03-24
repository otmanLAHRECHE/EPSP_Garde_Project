import os
import sqlite3

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTableWidget, QMessageBox

from dialogs import Add_new_inf, Saving_progress_dialog
from threads import ThreadAddGroupe
from tools import get_workers_count

basedir = os.path.dirname(__file__)


class UrgenceInfUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceInfUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'urgence_inf.ui'), self)

        self.tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.tab.setTabText(0, "Listes de garde")
        self.tab.setTabText(1, "Infirmiers survients")
        self.tab.setTabText(2, "Infirmiers")
        self.medcinname = self.findChild(QLineEdit, "lineEdit")
        self.add_garde = self.findChild(QPushButton, "pushButton_4")
        self.add_garde.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'plus.png')))

        self.add = self.findChild(QPushButton, "pushButton")
        self.add.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'plus.png')))
        self.update = self.findChild(QPushButton, "pushButton_3")
        self.update.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'edit.png')))
        self.delete = self.findChild(QPushButton, "pushButton_2")
        self.delete.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'user-x.png')))
        self.table = self.findChild(QTableWidget, "tableWidget")
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 110)

        self.table_group = self.findChild(QTableWidget, "tableWidget_3")
        self.table_group.setColumnWidth(0, 80)
        self.table_group.setColumnWidth(1, 200)
        self.table_group.setColumnWidth(2, 110)
        self.table_group.setColumnWidth(3, 110)

        self.add_group = self.findChild(QPushButton, "pushButton_7")
        self.add_group.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'plus.png')))
        self.update_group = self.findChild(QPushButton, "pushButton_6")
        self.update_group.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'edit.png')))
        self.delete_group = self.findChild(QPushButton, "pushButton_5")
        self.delete_group.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'user-x.png')))



        self.table_gardes = self.findChild(QTableWidget, "tableWidget_2")


        self.table_gardes.setColumnWidth(0, 150)
        self.table_gardes.setColumnWidth(1, 150)
        self.table_gardes.setColumnWidth(2, 150)
        self.table_gardes.setColumnWidth(3, 180)
        self.table_gardes.setColumnWidth(4, 270)
        self.table_gardes.hideColumn(0)

        self.loadGuardMonths()
        self.loadUsers()
        self.loadGroups()

        self.add.clicked.connect(self.add_toDb)
        self.delete.clicked.connect(self.deleteUser)
        self.update.clicked.connect(self.updateUser)
        self.add_garde.clicked.connect(self.add_grd)

        self.add_group.clicked.connect()
        self.delete_group.clicked.connect()
        self.update_group.clicked.connect()



    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def add_toDb(self):
        med_count = get_workers_count("urgence_surv")[0]
        if self.medcinname.text() == "":
            message = 'Le champ de nom est vide!'
            self.alert_(message)

        elif med_count[0] > 25:
            message = 'Maximum nombre des medecin, supremer un medecin'
            self.alert_(message)
        else:

            connection = sqlite3.connect("database/sqlite.db")
            cur = connection.cursor()
            sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
            med = (self.medcinname.text(), 'urgence_surv')
            cur.execute(sql_q, med)
            connection.commit()
            connection.close()
            self.medcinname.setText("")
            self.loadUsers()

    def add_to_groupe(self):
        med_count = get_workers_count("urgence_inf")[0]
        dialog_add = Add_new_inf()
        if dialog_add.exec() == QtWidgets.QDialog.Accepted:
            if dialog_add.nom == "":
                message = 'Le champ de nom est vide!'
                self.alert_(message)
            elif med_count[0] > 25:
                message = 'Maximum nombre des medecin, supremer un medecin'
                self.alert_(message)
            else:
                self.dialog = Saving_progress_dialog()
                self.dialog.label.setText("saving")
                self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.dialog.show()

                self.thr = ThreadAddGroupe(dialog_add.nom.text(), dialog_add.groupe.currentText())
                self.thr._signal.connect()
                self.thr._signal_result.connect()





        if self.medcinname.text() == "":
            message = 'Le champ de nom est vide!'
            self.alert_(message)

        elif med_count[0] > 25:
            message = 'Maximum nombre des medecin, supremer un medecin'
            self.alert_(message)
        else:

            connection = sqlite3.connect("database/sqlite.db")
            cur = connection.cursor()
            sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
            med = (self.medcinname.text(), 'urgence_surv')
            cur.execute(sql_q, med)
            connection.commit()
            connection.close()
            self.medcinname.setText("")
            self.loadUsers()

    def signal_accepted(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            print(progress)
            self.dialog.close()
            self.loadGroups()






