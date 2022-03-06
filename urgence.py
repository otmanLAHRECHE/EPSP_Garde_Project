import sqlite3

from PyQt5 import uic, QtWidgets, QtSql, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys

from dialogs import Update_worker_dialog
from widgets import Buttons


class UrgenceMainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceMainUi, self).__init__()
        uic.loadUi('ui/urgence.ui', self)

        self.tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.tab.setTabText(0, "Listes de garde")
        self.tab.setTabText(1, "Medecins")

        self.tab_gardes = self.findChild(QWidget, "tab")
        self.tab_medcines = self.findChild(QWidget, "tab_2")
        self.medcinname = self.findChild(QLineEdit, "lineEdit")
        self.add_garde = self.findChild(QPushButton, "pushButton_4")
        self.add_garde.setIcon(QIcon("asstes/images/plus.png"))

        self.add = self.findChild(QPushButton, "pushButton")
        self.add.setIcon(QIcon("asstes/images/plus.png"))
        self.update = self.findChild(QPushButton, "pushButton_3")
        self.update.setIcon(QIcon("asstes/images/edit.png"))
        self.delete = self.findChild(QPushButton, "pushButton_2")
        self.delete.setIcon(QIcon("asstes/images/user-x.png"))
        self.table = self.findChild(QTableWidget, "tableWidget")
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 110)

        self.table_gardes = self.findChild(QTableWidget, "tableWidget_2")

        self.table_gardes.setColumnWidth(0, 80)
        self.table_gardes.setColumnWidth(1, 100)
        self.table_gardes.setColumnWidth(2, 150)
        self.table_gardes.setColumnWidth(3, 180)
        self.table_gardes.setColumnWidth(4, 220)
        self.table_gardes.setCellWidget(0, 4, Buttons())

        self.loadGuardMonths()
        self.loadUsers()

        self.add.clicked.connect(self.add_toDb)
        self.delete.clicked.connect(self.deleteUser)
        self.update.clicked.connect(self.updateUser)

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def add_toDb(self):
        if self.medcinname.text() == "":
            message = 'Le champ de nom est vide!'
            self.alert_(message)
        else:
            connection = sqlite3.connect('database/sqlite.db')
            cur = connection.cursor()
            sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
            med = (self.medcinname.text(), 'urgence')
            cur.execute(sql_q, med)
            connection.commit()
            connection.close()
            self.medcinname.setText("")
            self.loadUsers()

    def deleteUser(self):
        row = self.table.currentRow()
        print(row)
        if row > -1:
            id = self.table.item(row, 0).text()
            connection = sqlite3.connect('database/sqlite.db')
            cur = connection.cursor()
            sql_q = 'DELETE FROM health_worker WHERE worker_id=?'
            cur.execute(sql_q, (id,))
            connection.commit()
            connection.close()
            self.table.setItem(row, 0, QTableWidgetItem(""))
            self.table.setItem(row, 1, QTableWidgetItem(""))
            self.table.setItem(row, 2, QTableWidgetItem(""))
            self.loadUsers()
        else:
            message = 'Selectioner un medecin'
            self.alert_(message)

    def updateUser(self):
        row = self.table.currentRow()
        print(row)
        if row > -1:
            dialog = Update_worker_dialog()
            print("dialog")
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                if dialog.worker.text() == "":
                    message = "enter un valide nom"
                    self.alert_(message)
                else:
                    id = self.table.item(row, 0).text()
                    connection = sqlite3.connect('database/sqlite.db')
                    cur = connection.cursor()
                    sql_q = 'UPDATE health_worker SET full_name= ? WHERE worker_id= ?'
                    cur.execute(sql_q, (dialog.worker.text(), id))
                    connection.commit()
                    connection.close()
                    self.loadUsers()

        else:
            message = 'Selectioner un medecin'
            self.alert_(message)

    def loadUsers(self):
        print("load users")
        connection = sqlite3.connect('database/sqlite.db')
        cur = connection.cursor()
        sql_q = 'SELECT * FROM health_worker where service=?'
        tablerow = 0
        cur.execute(sql_q, ('urgence',))
        results = cur.fetchall()
        for row in results:
            print(row)
            self.table.setItem(tablerow, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.table.setItem(tablerow, 2, QTableWidgetItem(row[2]))
            tablerow += 1
        self.table.setItem(tablerow, 0, QTableWidgetItem(""))
        self.table.setItem(tablerow, 1, QTableWidgetItem(""))
        self.table.setItem(tablerow, 2, QTableWidgetItem(""))
        connection.close()

    def loadGuardMonths(self):
        print("load guards")
        connection = sqlite3.connect('database/sqlite.db')
        cur = connection.cursor()
        sql_q = 'SELECT * FROM guard_mounth where service=?'
        tablerow = 0
        cur.execute(sql_q, ('urgence',))
        results = cur.fetchall()
        for row in results:
            print(row)
            self.table_gardes.insertRow(row)
            self.table_gardes.setRowHeight(row, 80)
            self.table_gardes.setItem(tablerow, 0, QTableWidgetItem(str(row[0])))
            self.table_gardes.setItem(tablerow, 1, QTableWidgetItem(str(row[1])))
            self.table_gardes.setItem(tablerow, 2, QTableWidgetItem(str(row[2])))
            self.table_gardes.setItem(tablerow, 3, QTableWidgetItem(row[3]))
            tablerow += 1
        connection.close()
